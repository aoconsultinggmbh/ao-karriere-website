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

// Mit &t=1: eine Testkarte anlegen und die Antwort von Asana zeigen.
if (($_GET['t'] ?? '') === '1' && !empty($wert) && is_string($wert)) {
    $koerper = ['data' => [
        'name'          => 'PRUEFKARTE bitte loeschen',
        'notes'         => 'Testkarte der Pruefseite.',
        'projects'      => ['1207775285258252'],
        'memberships'   => [['project' => '1207775285258252', 'section' => '1207775285258253']],
        'custom_fields' => [
            '1207919734281724' => 'pruef@example.org',
            '1207919734281726' => 'Pruefkarte',
            '1210066015972749' => ['date' => date('Y-m-d', strtotime('+6 months'))],
        ],
    ]];
    $c = curl_init('https://app.asana.com/api/1.0/tasks');
    curl_setopt_array($c, [
        CURLOPT_POST => true, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15,
        CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . trim($wert), 'Content-Type: application/json'],
        CURLOPT_POSTFIELDS => json_encode($koerper),
    ]);
    $a = curl_exec($c);
    echo "\n--- Testkarte anlegen ---\n";
    echo "HTTP " . curl_getinfo($c, CURLINFO_HTTP_CODE) . "\n";
    curl_close($c);
    echo substr((string)$a, 0, 1200) . "\n";
}
