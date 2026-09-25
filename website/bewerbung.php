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
antwort(true);
