<?php
/*
 * Bewerbung von der Karriereseite entgegennehmen und an die Personalabteilung
 * mailen. Laeuft nur auf dem echten Server (PHP), nicht in der GitHub-Vorschau.
 * Speichert nichts auf dem Server, die Anhaenge gehen direkt in die Mail.
 */
$EMPFAENGER    = 'jobs@ao-karriere.de';
$ABSENDER      = 'jobs@ao-karriere.de';   // muss eine echte Adresse AUF DIESER Domain sein,
                                         // sonst landet die Mail im Spam (SPF/DMARC)
$ABSENDER_NAME = 'AO Karriereseite';

/*
 * Bewerbermanagement in Asana (Board "BMS | #AO Consulting GmbH").
 * Der Zugriffsschluessel steht NICHT hier und nicht im GitHub-Projekt, sondern
 * in der Datei ao-geheim.php daneben. Die wird beim Hochladen ausgenommen und
 * ueberlebt damit jeden Upload. Fehlt sie, verhaelt sich das Skript wie frueher
 * und verschickt nur die Mail.
 */
$ASANA_DATEI     = __DIR__ . '/ao-geheim.php';
$ASANA_PROJEKT   = '1207775285258252';   // BMS | #AO Consulting GmbH
$ASANA_SPALTE    = '1207775285258253';   // Beworben
$ASANA_F_MAIL    = '1207919734281724';   // Feld "Mail"
$ASANA_F_NAME    = '1207919734281726';   // Feld "Name"
$ASANA_F_LOESCH  = '1210066015972749';   // Feld "Bewerber wird geloescht am"
$ASANA_FRIST     = '+6 months';          // Aufbewahrung, abgestimmt 30.09.2026

$MAX_GESAMT = 10 * 1024 * 1024;   // 10 MB ueber alle Anhaenge
$MAX_ANZAHL = 3;
// Ovidiu 25.09.2026: Bewerbungen grundsaetzlich als PDF.
$ERLAUBT = [
  'pdf'  => 'application/pdf',
];

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function antwort($ok, $fehler = '') {
    echo json_encode(['ok' => $ok, 'fehler' => $fehler], JSON_UNESCAPED_UNICODE);
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); antwort(false, 'Nur POST.'); }

// Honigtopf: Bots fuellen das unsichtbare Feld aus. Still "ok" melden, nichts senden.
if (!empty($_POST['webseite'])) antwort(true);

function feld($n, $max = 2000) {
    $v = isset($_POST[$n]) ? trim((string)$_POST[$n]) : '';
    $v = str_replace(["\r", "\n"], ' ', substr($v, 0, $max));
    return htmlspecialchars($v, ENT_QUOTES, 'UTF-8');
}
function mehrzeilig($n, $max = 4000) {
    $v = isset($_POST[$n]) ? trim((string)$_POST[$n]) : '';
    return htmlspecialchars(substr($v, 0, $max), ENT_QUOTES, 'UTF-8');
}

$name    = feld('name', 200);
$email   = isset($_POST['email']) ? trim((string)$_POST['email']) : '';
$telefon = feld('telefon', 60);
$stelle  = feld('stelle', 200);
$text    = mehrzeilig('nachricht');

if ($name === '')                                     antwort(false, 'Name fehlt.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL))       antwort(false, 'E-Mail-Adresse ist ungueltig.');
// Telefon ist Pflicht (Ovidiu 25.09.2026), mindestens sechs Ziffern.
if (preg_match_all('/\d/', $telefon) < 6)             antwort(false, 'Bitte eine Telefonnummer angeben.');
if ($stelle === '')                                   antwort(false, 'Stelle fehlt.');
if (empty($_POST['datenschutz']))                     antwort(false, 'Einwilligung fehlt.');
$email = htmlspecialchars($email, ENT_QUOTES, 'UTF-8');

/* ---------- Anhaenge einsammeln und pruefen ---------- */
$anhaenge = [];
$summe = 0;
if (!empty($_FILES['unterlagen']['name'][0])) {
    $n = count($_FILES['unterlagen']['name']);
    if ($n > $MAX_ANZAHL) antwort(false, 'Hoechstens drei Dateien.');
    for ($i = 0; $i < $n; $i++) {
        if ($_FILES['unterlagen']['error'][$i] === UPLOAD_ERR_NO_FILE) continue;
        if ($_FILES['unterlagen']['error'][$i] !== UPLOAD_ERR_OK) antwort(false, 'Eine Datei kam nicht vollstaendig an.');
        $tmp  = $_FILES['unterlagen']['tmp_name'][$i];
        if (!is_uploaded_file($tmp)) antwort(false, 'Datei abgelehnt.');
        $roh  = $_FILES['unterlagen']['name'][$i];
        $endung = strtolower(pathinfo($roh, PATHINFO_EXTENSION));
        if (!isset($ERLAUBT[$endung])) antwort(false, 'Bitte nur PDF-Dateien anhängen.');
        // Nicht nur der Name zaehlt: jede echte PDF-Datei beginnt mit %PDF.
        $anfang = @file_get_contents($tmp, false, null, 0, 5);
        if ($anfang !== '%PDF-') antwort(false, 'Eine der Dateien ist kein gültiges PDF.');
        $groesse = filesize($tmp);
        $summe += $groesse;
        if ($summe > $MAX_GESAMT) antwort(false, 'Die Dateien sind zusammen groesser als 10 MB.');
        // Dateiname entschaerfen: nur Buchstaben, Ziffern, Punkt, Strich
        $sicher = preg_replace('/[^A-Za-z0-9._-]/', '_', $roh);
        $sicher = substr($sicher, 0, 120);
        $anhaenge[] = [
            'name' => $sicher,
            'typ'  => $ERLAUBT[$endung],
            'daten'=> file_get_contents($tmp),
        ];
    }
}

/* ---------- Mail bauen ---------- */
$betreff = 'Bewerbung: ' . $stelle . ' — ' . $name;
$zeilen = [
    'Neue Bewerbung ueber ao-karriere.de',
    '',
    'Stelle:   ' . $stelle,
    'Name:     ' . $name,
    'E-Mail:   ' . $email,
    'Telefon:  ' . $telefon,
    'Anhaenge: ' . (count($anhaenge) ? count($anhaenge) . ' (' . implode(', ', array_column($anhaenge, 'name')) . ')' : 'keine'),
    '',
    'Nachricht:',
    ($text !== '' ? $text : '(keine)'),
    '',
    '---',
    'Gesendet am ' . date('d.m.Y H:i') . ' Uhr',
];
$koerper = implode("\r\n", $zeilen);

$grenze = '=_ao_' . bin2hex(random_bytes(12));
$kopf  = 'From: ' . mb_encode_mimeheader($ABSENDER_NAME, 'UTF-8') . ' <' . $ABSENDER . ">\r\n";
$kopf .= 'Reply-To: ' . $email . "\r\n";
$kopf .= "MIME-Version: 1.0\r\n";
$kopf .= 'Content-Type: multipart/mixed; boundary="' . $grenze . '"' . "\r\n";

$rumpf  = '--' . $grenze . "\r\n";
$rumpf .= "Content-Type: text/plain; charset=UTF-8\r\n";
$rumpf .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
$rumpf .= $koerper . "\r\n";
foreach ($anhaenge as $a) {
    $rumpf .= '--' . $grenze . "\r\n";
    $rumpf .= 'Content-Type: ' . $a['typ'] . '; name="' . $a['name'] . '"' . "\r\n";
    $rumpf .= "Content-Transfer-Encoding: base64\r\n";
    $rumpf .= 'Content-Disposition: attachment; filename="' . $a['name'] . '"' . "\r\n\r\n";
    $rumpf .= chunk_split(base64_encode($a['daten'])) . "\r\n";
}
$rumpf .= '--' . $grenze . "--\r\n";

$gesendet = @mail($EMPFAENGER, mb_encode_mimeheader($betreff, 'UTF-8'), $rumpf, $kopf, '-f' . $ABSENDER);
if (!$gesendet) { http_response_code(500); antwort(false, 'Versand fehlgeschlagen.'); }

/* ---------- Karte im Bewerbermanagement anlegen ----------
 * Zweiter Schritt, bewusst NACH der Mail. Geht hier etwas schief, merkt der
 * Bewerber davon nichts und die Bewerbung ist trotzdem angekommen. Der Fehler
 * landet im Serverprotokoll, damit man ihn nachtraeglich findet.
 */
function asana_ruf($schluessel, $pfad, $daten, $datei = null, $sekunden = 10) {
    $c = curl_init('https://app.asana.com/api/1.0/' . $pfad);
    $kopf = ['Authorization: Bearer ' . $schluessel, 'Accept: application/json'];
    if ($datei === null) {
        $kopf[] = 'Content-Type: application/json';
        curl_setopt($c, CURLOPT_POSTFIELDS, json_encode(['data' => $daten]));
    } else {
        curl_setopt($c, CURLOPT_POSTFIELDS, $datei);   // multipart, Content-Type setzt cURL
    }
    curl_setopt_array($c, [
        CURLOPT_POST           => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => $kopf,
        CURLOPT_TIMEOUT        => $sekunden,
        CURLOPT_CONNECTTIMEOUT => 5,
    ]);
    $antwort = curl_exec($c);
    $code    = curl_getinfo($c, CURLINFO_HTTP_CODE);
    curl_close($c);
    return [$code, json_decode((string)$antwort, true)];
}

function asana_karte($daten) {
    if (!function_exists('curl_init')) return;
    if (!is_readable($daten['datei'])) return;            // kein Schluessel hinterlegt
    $schluessel = @include $daten['datei'];
    $schluessel = is_string($schluessel) ? trim($schluessel) : '';
    if ($schluessel === '') return;

    $notiz = "Stelle: " . $daten['stelle'] . "\n"
           . "Telefon: " . $daten['telefon'] . "\n"
           . "E-Mail: " . $daten['email'] . "\n\n"
           . "Nachricht:\n" . ($daten['text'] !== '' ? $daten['text'] : '(keine)') . "\n\n"
           . "Eingegangen ueber ao-karriere.de am " . date('d.m.Y H:i') . " Uhr.";

    list($code, $ergebnis) = asana_ruf($schluessel, 'tasks', [
        'name'          => $daten['name'],
        'notes'         => $notiz,
        'projects'      => [$daten['projekt']],
        'memberships'   => [['project' => $daten['projekt'], 'section' => $daten['spalte']]],
        'custom_fields' => [
            $daten['f_mail']   => $daten['email'],
            $daten['f_name']   => $daten['name'],
            // Datumsfelder verlangt Asana als Objekt, nicht als Text:
            // {"date": "2027-03-30"}. Als blosser Text antwortet die
            // Schnittstelle mit 400 "DayAndDateTime is not a JSON object".
            $daten['f_loesch'] => ['date' => date('Y-m-d', strtotime($daten['frist']))],
        ],
    ]);
    if ($code < 200 || $code > 299 || empty($ergebnis['data']['gid'])) {
        error_log('Bewerbung: Asana-Karte fuer "' . $daten['name'] . '" nicht angelegt (HTTP ' . $code . ').');
        return;
    }
    $aufgabe = $ergebnis['data']['gid'];

    foreach ($daten['anhaenge'] as $a) {
        // Nicht die hochgeladene Datei verwenden: die raeumt PHP weg, sobald die
        // Antwort an den Browser raus ist. Die Bytes liegen ohnehin schon im
        // Arbeitsspeicher, daraus wird hier kurz eine eigene Datei geschrieben.
        if (empty($a['daten'])) continue;
        $weg = tempnam(sys_get_temp_dir(), 'ao');
        if ($weg === false) continue;
        file_put_contents($weg, $a['daten']);
        list($code2,) = asana_ruf($schluessel, 'attachments', null, [
            'parent' => $aufgabe,
            'file'   => new CURLFile($weg, $a['typ'], $a['name']),
        ], 60);
        @unlink($weg);
        if ($code2 < 200 || $code2 > 299) {
            error_log('Bewerbung: Anhang "' . $a['name'] . '" nicht an Asana-Karte '
                      . $aufgabe . ' gehaengt (HTTP ' . $code2 . ').');
        }
    }
}

/*
 * Erst dem Browser antworten, dann Asana. Sonst wartet der Bewerber auf einen
 * Schritt, der ihn nichts angeht, und bei einem langsamen Anhang laeuft die
 * Zeit fuer das Skript ab, bevor die Antwort ankommt: Er sieht eine
 * Fehlermeldung, obwohl die Mail laengst raus ist.
 */
ignore_user_abort(true);
// Kein eigenes Content-Length und kein Connection-Header: wenn der Server die
// Antwort komprimiert, stimmt die angegebene Laenge nicht mehr und der Browser
// verwirft die Antwort. fastcgi_finish_request genuegt, um die Verbindung zu
// schliessen und im Hintergrund weiterzuarbeiten.
echo json_encode(['ok' => true, 'fehler' => ''], JSON_UNESCAPED_UNICODE);
while (ob_get_level() > 0) { @ob_end_flush(); }
@flush();
if (function_exists('fastcgi_finish_request')) { @fastcgi_finish_request(); }
@set_time_limit(120);   // der Rest laeuft ohne Zuschauer weiter

try {
    asana_karte([
        'datei' => $ASANA_DATEI, 'projekt' => $ASANA_PROJEKT, 'spalte' => $ASANA_SPALTE,
        'f_mail' => $ASANA_F_MAIL, 'f_name' => $ASANA_F_NAME, 'f_loesch' => $ASANA_F_LOESCH,
        'frist' => $ASANA_FRIST, 'name' => $name, 'email' => $email, 'telefon' => $telefon,
        'stelle' => $stelle, 'text' => $text, 'anhaenge' => $anhaenge,
    ]);
} catch (Throwable $e) {
    error_log('Bewerbung: Asana-Schritt abgebrochen: ' . $e->getMessage());
}
exit;
