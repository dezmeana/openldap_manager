# File: ldif2csv-StoogesDumpAll.awk
# Create csv dump for whole database
#
BEGIN {
        last       = ""
        first      = ""
        name       = ""
        uidNumber  = ""
        printf(" last,first,full name,uidNumber\n");
}
/^sn: /              {last=$2}
/^givenName: /       {first=$2}
/^cn: /              {name=$2}
/^uidNumber: /       {uidNumber=$2}
/^gidNumber: /       {gidNumber=$2}
/^dn/ {
        if(last != "" && first != "" && last != "StoogeAdmin") printf("%s,%s,%s,%s,%s\n",last,first,name,uidNumber,gidNumber)
        last       = ""
        first      = ""
        name       = ""
        uidNumber  = ""
        uidNumber  = ""
}
# Capture last dn
END {
        if(last != "" && first != "" && last != "StoogeAdmin") printf("%s,%s,%s,%s,%s\n",last,first,name,uidNumber,gidNumber)
}
