x = input("database name:")
y = input("columns (type: name,password)").split(",")
a=""
b=""
c=""
d=""
e=""
f=""
g=""

def remove_last_char(word):
    return word[:-1]

for i in range(len(y)):
    a+="$"+y[i]+","
    b+=":"+y[i]+","
    c+=y[i]+","
    d+='$add->bindValue(":'+y[i]+'", htmlspecialchars($'+y[i]+'));\n'
    e+=",$"+y[i]+" = null"
    f+='"'+y[i]+'",'
    g+="""
    \n
    if (!empty($"""+y[i]+""")) {
        $fieldsToUpdate[] = '"""+y[i]+""" = :"""+y[i]+"""';
        $bindParams[":"""+y[i]+""""] = htmlspecialchars($"""+y[i]+""");
    }
    \n
    """
    pass








code = """

<?php
include "../database.php";

class """+x+"""_database
{
    private $db; 

    public function __construct($db)
    {
        $this->db = $db; 
    }

    public function add("""+remove_last_char(a)+""")
    {
        try {
            $addingTime = date("Y-m-d H:i:s");
            $updateTime = date("Y-m-d H:i:s");

            $add = $this->db->prepare("INSERT INTO """+x+""" ("""+c+""" adding_time, update_time) 
                                       VALUES ("""+b+""" :adding_time, :update_time)");
            
            """+d+"""

            $add->bindValue(":adding_time", $addingTime);
            $add->bindValue(":update_time", $updateTime);

            return $add->execute(); 

        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function pull()
    {
        try {
            $pull = $this->db->prepare("SELECT * FROM """+x+"""");
            $pull->execute();
            $result = $pull->fetchAll(PDO::FETCH_ASSOC);
            return json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE); 

        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function delete($id)
    {
        try {
            $delete = $this->db->prepare("DELETE FROM """+x+""" WHERE id=:id");
            $delete->bindValue(":id", $id, PDO::PARAM_INT);
            return $delete->execute();

        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }




    

    public function update($forWhere, $forWhereValue  """+e+""")
    {
        try {
            $validColumns = ["id", """+f+""" "adding_time", "update_time"];
            if (!in_array($forWhere, $validColumns)) {
                return "invalid column name!";
            }

            $fieldsToUpdate = [];
            $bindParams = [];

            """+g+"""


            $fieldsToUpdate[] = "update_time = :update_time";
            $bindParams[":update_time"] = date("Y-m-d H:i:s");

            if (count($fieldsToUpdate) == 0) { 
                return "No data entered to update!";
            }

            $sql = "UPDATE """+x+""" SET " . implode(", ", $fieldsToUpdate) . " WHERE $forWhere = :forWhereValue";
            $update = $this->db->prepare($sql);

            foreach ($bindParams as $key => $value) {
                $update->bindValue($key, $value);
            }
            $update->bindValue(":forWhereValue", $forWhereValue);

            return $update->execute();

        } catch (Exception $e) {
            return "Hata: " . $e->getMessage();
        }
    }
}
?>


"""

filename = f"dbs/{x}_database.php"
with open(filename, "w") as file:
    file.write(code)

print(f"{filename} created successfully")
