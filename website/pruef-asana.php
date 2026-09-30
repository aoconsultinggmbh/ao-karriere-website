<?php
/*
 * Voruebergehende Pruefseite fuer die Asana-Anbindung. Zeigt nur, OB der
 * Schluessel da ist und was Asana antwortet - nie den Schluessel selbst.
 * Wird nach der Pruefung wieder aus dem Projekt entfernt.
 */
if (($_GET['k'] ?? '') !== 'w7q2n5') { http_response_code(404); exit; }
header('Content-Type: text/plain; charset=utf-8');

$datei = __DIR__ . '/ao-geheim.php';
echo "Datei ao-geheim.php vorhanden: " . (file_exists($datei) ? 'ja' : 'NEIN') . "\n";
echo "Datei lesbar: " . (is_readable($datei) ? 'ja' : 'NEIN') . "\n";
if (file_exists($datei)) {
    echo "Dateigroesse: " . filesize($datei) . " Zeichen\n";
    $wert = @include $datei;
    echo "Rueckgabe ist Text: " . (is_string($wert) ? 'ja' : 'NEIN (' . gettype($wert) . ')') . "\n";
    if (is_string($wert)) echo "Laenge des Schluessels: " . strlen(trim($wert)) . " Zeichen\n";
}
echo "cURL vorhanden: " . (function_exists('curl_init') ? 'ja' : 'NEIN') . "\n";

if (!empty($wert) && is_string($wert) && function_exists('curl_init')) {
    $c = curl_init('https://app.asana.com/api/1.0/users/me');
    curl_setopt_array($c, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . trim($wert)],
        CURLOPT_TIMEOUT => 10,
    ]);
    $a = curl_exec($c);
    echo "Antwort von Asana: HTTP " . curl_getinfo($c, CURLINFO_HTTP_CODE) . "\n";
    if ($a === false) echo "cURL-Fehler: " . curl_error($c) . "\n";
    curl_close($c);
    $j = json_decode((string)$a, true);
    if (isset($j['data']['name'])) echo "Angemeldet als: " . $j['data']['name'] . "\n";
    if (isset($j['errors'][0]['message'])) echo "Fehlermeldung: " . $j['errors'][0]['message'] . "\n";
}
