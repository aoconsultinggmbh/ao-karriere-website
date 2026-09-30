<?php
// Voruebergehend: prueft nur den Anhang-Upload zu Asana. Kommt danach wieder weg.
if (($_GET['k'] ?? '') !== 'w7q2n5') { http_response_code(404); exit; }
header('Content-Type: text/plain; charset=utf-8');
$wert = @include __DIR__ . '/ao-geheim.php';
if (!is_string($wert)) { echo "kein Schluessel\n"; exit; }
$s = trim($wert);

$aufgabe = $_GET['a'] ?? '';
if ($aufgabe === '') { echo "Bitte &a=<Aufgaben-ID> angeben\n"; exit; }

$tmp = tempnam(sys_get_temp_dir(), 'pdf');
file_put_contents($tmp, "%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n");
echo "Testdatei: " . $tmp . " (" . filesize($tmp) . " Bytes, lesbar: " . (is_readable($tmp)?'ja':'nein') . ")\n";

$c = curl_init('https://app.asana.com/api/1.0/attachments');
curl_setopt_array($c, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $s, 'Accept: application/json'],
    CURLOPT_POSTFIELDS => ['parent' => $aufgabe, 'file' => new CURLFile($tmp, 'application/pdf', 'Pruef.pdf')],
]);
$a = curl_exec($c);
echo "HTTP " . curl_getinfo($c, CURLINFO_HTTP_CODE) . "\n";
if ($a === false) echo "cURL-Fehler: " . curl_error($c) . "\n";
curl_close($c);
@unlink($tmp);
echo substr((string)$a, 0, 800) . "\n";
