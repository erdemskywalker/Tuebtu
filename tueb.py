import sys
import os


code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tueb</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.js" integrity="sha256-eKhayi8LEQwp4NKxN+CfCh+3qOVUtJn3QNZ0TciWLP4=" crossorigin="anonymous"></script>
    <style>
        body{
            background: -webkit-linear-gradient(0deg,rgb(156, 69, 134),rgb(136, 39, 39));
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        section{
            position: fixed; 
            top: 0;
            left: 0;
            width: 100vw; 
            height: 100vh; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }

        section *{
            margin-top: 50px;
            font-weight: 100;
        }

        section .hood{
            font-size: 100px;
            font-weight: 200;
        }

        @media screen and (max-width: 590px){
            section .hood{
                font-size: 50px;
                font-weight: 200;
            }
        }

       
    </style>
</head>
<body>
    <section>
        <h1>hiii, I am a blank page (:</h1>
        <h1 class="hood">TUEB FRAMEWORK</h1>
        <div class="" id="a">
            <button #click('https://github.com/erdemskywalker') type="button" id="Btn1" class="btn btn-dark">GIT HUB</button>
        </div>
        <p>WE ARE HERE FOR YOUR CURIOUSNESS</p>
    </section>
    @erdemskywalker
</body>
</html>
"""


def run():
    os.system('php -S localhost:8000 -t "'+os.getcwd()+'"')

def newmodel():
    x=input("Model Name:")

    filename = f"models/{x}.model.php"
    with open(filename, "w") as file:
        file.write("""<?php

include "sql.php";

$tableName = '"""+x+"""';
$columns = [
    
];

$"""+x+"""TabloModel = new DynamicTable($db, $tableName, $columns);

?>
        """)
    print(f"{filename} created successfully")

def newpage():
    x=input("Pages Name:")

    filename = f"views/{x}.php"
    with open(filename, "w") as file:
        file.write(code)
    print(f"{filename} created successfully")


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Kullanım: python tueb.py <run|newpage|newmodel>")
        sys.exit(1)

    command = args[1]

    if command == "run":
        run()
    elif command == "newpage":
        newpage()
    elif command == "newmodel":
        newmodel()
    else:
        print("Geçersiz komut!")