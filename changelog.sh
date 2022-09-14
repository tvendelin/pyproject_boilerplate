usage(){
    cat <<EOU
    
    Creates debian/changelog file based on annotated git tags 

    Usage: sh $0

    Requirement:
    Python module toml-cli

    As using this script makes sense only in relation to existing Python project
    defined with pyproject.toml, you should probably add toml-cli package to
    project's (optional) dependencies, and then install your project into 
    a virtual environment. You can also install it manually by running

    pip install toml-cli

EOU

}

if ! which -s toml; then
    usage && exit 1
fi

project_name(){
    toml get --toml-path pyproject.toml project.name
}

PROJECT_NAME=$(project_name)

git tag -l --sort=-version:refname | while read T
 do 
    git tag -l  --format="$PROJECT_NAME (%(tag)) all; urgency=medium" "$T"
    echo ''
    git tag -l --format="* %(subject)" "$T"|sed -e 's/^/  /'
    git tag -l --format="%(body)" "$T"|sed -e 's/^/    /'
    git tag -l --format="%(taggername) %(taggeremail)  %(taggerdate)" "$T"
    echo ''
 done
