#!/bin/sh
echo "Content-type: application/json"
echo ""
read POST_DATA
get_schedules() {
    echo "["
    first=1
    crontab -l | grep "adguardhome" | while read -r line; do
        if [ "$first" -eq 0 ]; then echo ","; fi
        
        min=$(echo "$line" | awk '{print $1}')
        hour=$(echo "$line" | awk '{print $2}')
        dow=$(echo "$line" | awk '{print $5}')
        
        if echo "$line" | grep -q "enabled\": true"; then
            action="ON"
        else
            action="OFF"
        fi
        
        id=$(echo "$line" | md5sum | awk '{print $1}')
        
        echo "{\"id\": \"$id\", \"hour\": \"$hour\", \"min\": \"$min\", \"dow\": \"$dow\", \"action\": \"$action\"}"
        first=0
    done
    echo "]"
}
# Helper to generate the Cron Line
make_cron_line() {
    m=$1; h=$2; d=$3; a=$4
    
    if [ "$a" = "ON" ]; then bool="true"; else bool="false"; fi
    cmd="curl -X POST -H \"Content-Type: application/json\" -d '{\"enabled\": $bool}' http://127.0.0.1:3000/control/filtering/config >/dev/null 2>&1"
    
    if [ -z "$d" ]; then d="*"; fi
    echo "$m $h * * $d $cmd # adguardhome"
}
add_schedule() {
    # Parse params
    hour=$(echo "$QUERY_STRING" | grep -o 'hour=[0-9]*' | cut -d= -f2)
    min=$(echo "$QUERY_STRING" | grep -o 'min=[0-9]*' | cut -d= -f2)
    action=$(echo "$QUERY_STRING" | grep -o 'action=[A-Z]*' | cut -d= -f2)
    days=$(echo "$QUERY_STRING" | grep -o 'days=[a-zA-Z0-9,]*' | cut -d= -f2)
    if [ -z "$hour" ] || [ -z "$min" ] || [ -z "$action" ]; then
        echo "{\"status\": \"error\", \"message\": \"Missing parameters\"}"
        return
    fi
    
    line=$(make_cron_line "$min" "$hour" "$days" "$action")
    (crontab -l 2>/dev/null; echo "$line") | crontab -
    
    echo "{\"status\": \"success\"}"
}
delete_schedule_internal() {
    did=$1
    tmp="/tmp/cron.tmp"
    crontab -l > "$tmp"
    mv "$tmp" "$tmp.old"
    touch "$tmp"
    
    while read -r line; do
        lid=$(echo "$line" | md5sum | awk '{print $1}')
        if [ "$lid" = "$did" ] && echo "$line" | grep -q "adguardhome"; then
            continue
        fi
        echo "$line" >> "$tmp"
    done < "$tmp.old"
    
    crontab "$tmp"
    rm "$tmp" "$tmp.old"
}
delete_schedule() {
    id=$(echo "$QUERY_STRING" | grep -o 'id=[a-z0-9]*' | cut -d= -f2)
    delete_schedule_internal "$id"
    echo "{\"status\": \"success\"}"
}
edit_schedule() {
    # Delete Old
    old_id=$(echo "$QUERY_STRING" | grep -o 'id=[a-z0-9]*' | cut -d= -f2)
    delete_schedule_internal "$old_id"
    
    # Add New
    add_schedule
}
mode=$(echo "$QUERY_STRING" | grep -o 'mode=[a-z]*' | cut -d= -f2)
case "$mode" in
    add) add_schedule ;;
    del) delete_schedule ;;
    edit) edit_schedule ;;
    list) get_schedules ;;
    *) echo "{\"error\": \"Unknown mode\"}" ;;
esac
