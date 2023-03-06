<?

header('Access-Control-Allow-Origin: http://localhost:5173');//No caso o link do servidor poderá ser alterado(porta)
    header('Access-Control-Allow-Credentials: true');


$dsn = 'mysql:dbname=ReLUZ;host=localhost;port=3306';//porta pode ser alterada
    $conn = new PDO($dsn, 'root', 'root');

    session_start();

?>