# Source data dirname
dir="data"

# Download & extract sources into the data dir
function get_files {
	rm -rf $dir
	mkdir $dir
	cd $dir
	
	case $1 in
		small) name="ml-latest-small";;
		medium) name="ml-latest";;
		stable) name="ml-25m";;
	esac
	
	curl -o "${name}.zip" "https://files.grouplens.org/datasets/movielens/${name}.zip"
	unzip -p "${name}.zip" "${name}/movies.csv" > movies.csv
	unzip -p "${name}.zip" "${name}/ratings.csv" > ratings.csv
	rm "${name}.zip"
}

# Get CLI argument
while [ -n "$1" ]
do
	case "$1" in
		--ds) param="$2"
		shift ;;		
		*) echo "Usage: setup.sh --ds small|medium|stable"
		exit 1 ;;
	esac
	shift
done

# Specify download file
case $param in
    small) get_files "small";;
	medium) get_files "medium";;
	stable) get_files "stable";;
	*) echo "Usage: setup.sh --ds small|medium|stable" 
esac
