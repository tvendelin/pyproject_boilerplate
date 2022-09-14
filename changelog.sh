git tag -l --sort=-version:refname | while read T
 do 
    git tag -l  --format='Myproject (%(tag)) all; urgency=medium' "$T"
    echo ''
    git tag -l --format="* %(subject)" "$T"|sed -e 's/^/  /'
    git tag -l --format="%(body)" "$T"|sed -e 's/^/  /'
    git tag -l --format="%(taggername) %(taggeremail)  %(taggerdate)" "$T"
    echo ''
 done
