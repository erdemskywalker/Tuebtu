<?php

include "../database.php";

$allowed_referers = ["deneme.model.php"]; 
$current_file = basename($_SERVER['PHP_SELF']);

if (!defined('TUEBTU_MODELS_IN') && in_array($current_file,$allowed_referers)) {
    http_response_code(403);
    error_log("unexpected request");
    die;
}

session_start();

if(isset($_SESSION["user"])){
    $myPermission=$_SESSION["user"]["statu"];
}else{
    $myPermission="guest";
}


class DynamicTable {
    private $db;
    private $tableName;
    private $columns;
    private $query;
    private $params = [];


    public function __construct($db, $tableName, $columns) 
    {
        if(isset($_SESSION["admin"])){$control=true;}else{$control=false;}
        $this->db = $db;
        $this->tableName = $tableName;
        $this->columns = $columns;
        $this->createTableIfNotExists();
        $this->query = "SELECT * FROM `$this->tableName` WHERE 1=1";
    }

    private function createTableIfNotExists() {
        
            $query = "CREATE TABLE IF NOT EXISTS `$this->tableName` (";
            $query .= "`id` INT AUTO_INCREMENT PRIMARY KEY, ";
            foreach ($this->columns as $columnName => $columnType) {
                $query .= "`$columnName` $columnType, ";
            }
            $query .= "`adding_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ";
            $query .= "`update_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP";
            $query .= ")";
            $this->db->exec($query);
    }

    public function add($data) {
        try {
            $columns = implode(", ", array_keys($data));
            $values = ":" . implode(", :", array_keys($data));
            $stmt = $this->db->prepare("INSERT INTO `$this->tableName` ($columns) VALUES ($values)");
            foreach ($data as $key => $value) {
                $stmt->bindValue(":$key", htmlspecialchars($value));
            }
            return $stmt->execute();
        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function all($limit = 50, $offset = 0) {
        try {
            $query = "SELECT * FROM `$this->tableName` LIMIT :limit OFFSET :offset";
            $stmt = $this->db->prepare($query);
            $stmt->bindValue(":limit", (int)$limit, PDO::PARAM_INT);
            $stmt->bindValue(":offset", (int)$offset, PDO::PARAM_INT);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function find($column, $value) {
        return $this->where($column, $value)->getOne();
    }

    public function where($column, $value, $operator = '=') {
        $this->query .= " AND `$column` $operator :$column";
        $this->params[":$column"] = htmlspecialchars($value);
        return $this;
    }

    public function like($column, $value) {
        return $this->where($column, "%$value%", "LIKE");
    }

    public function get() {
        try {
            $stmt = $this->db->prepare($this->query);
            foreach ($this->params as $key => $value) {
                $stmt->bindValue($key, $value);
            }
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function getOne() {
        try {
            $stmt = $this->db->prepare($this->query);
            foreach ($this->params as $key => $value) {
                $stmt->bindValue($key, $value);
            }
            $stmt->execute();
            return $stmt->fetch(PDO::FETCH_ASSOC);
        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function update($column, $value, $data) {
        try {
            $fieldsToUpdate = [];
            $bindParams = [":value" => htmlspecialchars($value)];
            foreach ($data as $key => $val) {
                $fieldsToUpdate[] = "`$key` = :$key";
                $bindParams[":$key"] = htmlspecialchars($val);
            }
            if (count($fieldsToUpdate) == 0) return "No fields to update!";
            $query = "UPDATE `$this->tableName` SET " . implode(", ", $fieldsToUpdate) . " WHERE `$column` = :value";
            $stmt = $this->db->prepare($query);
            foreach ($bindParams as $key => $val) {
                $stmt->bindValue($key, $val);
            }
            return $stmt->execute();
        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }

    public function delete($column, $value) {
        try {
            $stmt = $this->db->prepare("DELETE FROM `$this->tableName` WHERE `$column` = :value");
            $stmt->bindValue(":value", htmlspecialchars($value));
            return $stmt->execute();
        } catch (Exception $e) {
            return "Error: " . $e->getMessage();
        }
    }
}


function encode($data){
    $method = 'AES-128-ECB';
    $key = 'ornek_anahtar';
    return openssl_encrypt($data, $method, $key);
}

function decode($data){
    $method = 'AES-128-ECB';
    $key = 'ornek_anahtar';
    return openssl_decrypt($data, $method, $key);
}

function password_hash_encode($data){
    password_hash($data,PASSWORD_ARGON2I);
}

function password_hash_decode($data){
    password_verify($data,PASSWORD_ARGON2I);
}



?>
