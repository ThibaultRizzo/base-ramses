
######################
###### METHODS #######
######################

start() {
    local container_name="ramses-db"
    log sync "Starting docker stack..."
    docker-compose up -d $container_name
}

start_with_dump() {
    local container_name="ramses-db"
    local db_name="ramses"
    start

    poetry shell
    alembic upgrade head

    log sync "Applying dump..."
    local db_container_id=$(docker ps -aqf name="$container_name")
    docker exec $db_container_id psql -f dump.sql -U test -p 5432 $db_name
}

dump() {
    log sync "Creating dump..."
    local container_name="ramses-db"
    local db_name="ramses"
    local db_container_id=$(docker ps -aqf name="$container_name")

    docker exec $db_container_id pg_dump -a -f dump.sql -U test -p 5432 $db_name
    docker cp $db_container_id:/dump.sql dump.sql
}



################################
###### TECHNICAL METHODS #######
################################

log(){ _log_with_method _colorized_echo_e $@; }

logf(){  _log_with_method _colorized_echo_en $@; }

_log_with_method(){
    method=$1
    shift
    case $1 in
        info) shift && $method INFO 253 $@;;
        debug) shift && $method INFO 171 $@;;
        exec) shift && $method EXEC 39 $@;;
        sync) shift && $method SYNC 147 $@;;
        success) shift && $method OK 83 $@;;
        warning) shift && $method WARN 215 $@;;
        error) shift && $method ERROR 205 $@;;
        *)
            $method INFO 253 $@
            ;;
    esac

}

_colorized_echo_e(){
    local label="$1"
    local color="$2m"
    shift && shift
    local target="\x1B[0m\x1B[1m\x1B[38;5;208m\x1B[48;5;256m${TARGET}${remote} "
    local label=" " #\x1B[0m\x1B[1m\x1B[48;5;256m\x1B[38;5;${color}<SHEL[${label}]> "
    local value="\x1B[0m\x1B[1m\x1B[48;5;256m > \x1B[38;5;${color}$@ "
    echo "\x1B[0m${label}${value}\x1B[0m"
}

_colorized_echo_en(){
    local color="$2m"
    shift && shift
    local label="" #"\x1B[1m\x1B[38;5;231m\x1B[48;5;256m[ DO $label ]\x1B[0m "
    local value="\x1B[1m\x1B[48;5;256m\x1B[38;5;$color$@\x1B[0m "
    echo -e "\x1B[0m$label$value\x1B[0m"
}

$@

