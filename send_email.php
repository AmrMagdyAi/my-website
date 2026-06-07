<?php
/**
 * Contact form mailer — amrmagdy.com
 *
 * IMPORTANT: If mail() still fails after this fix, your hosting provider
 * has disabled PHP mail(). Use the Web3Forms method instead (see README).
 *
 * Quick diagnostics: visit /send_email.php?test=1 in your browser to check
 * whether PHP mail() works on your server.
 */

ini_set('display_errors', 0);
error_reporting(0);

header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');

/* ── Diagnostic test endpoint ──────────────────────── */
if (isset($_GET['test'])) {
    $testResult = @mail(
        'info@amrmagdy.com',
        'PHP mail() test — amrmagdy.com',
        "This is a test email to verify PHP mail() works on this server.\n\nSent: " . date('Y-m-d H:i:s T'),
        "From: info@amrmagdy.com\r\nContent-Type: text/plain; charset=UTF-8\r\n"
    );
    $error = error_get_last();
    header('Content-Type: text/plain');
    echo $testResult
        ? "✓ PHP mail() is working — check info@amrmagdy.com for the test email."
        : "✗ PHP mail() FAILED on this server.\n\nError: " . ($error['message'] ?? 'unknown') . "\n\nSolution: Use Web3Forms instead (see send_email_web3forms.php).";
    exit;
}

/* ── Only accept POST ───────────────────────────────── */
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed.']);
    exit;
}

/* ── Honeypot ───────────────────────────────────────── */
if (!empty($_POST['website'])) {
    echo json_encode(['success' => true]);
    exit;
}

/* ── Rate limiting ──────────────────────────────────── */
if (session_status() === PHP_SESSION_NONE) session_start();
$now = time();
if (isset($_SESSION['last_contact']) && ($now - $_SESSION['last_contact']) < 60) {
    http_response_code(429);
    echo json_encode(['success' => false, 'message' => 'Please wait a moment before sending again.']);
    exit;
}

/* ── Sanitise & validate ────────────────────────────── */
$name    = trim(filter_var($_POST['name']    ?? '', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
$email   = trim(filter_var($_POST['email']   ?? '', FILTER_SANITIZE_EMAIL));
$message = trim(filter_var($_POST['message'] ?? '', FILTER_SANITIZE_FULL_SPECIAL_CHARS));

if (!$name || !$email || !$message) {
    http_response_code(422);
    echo json_encode(['success' => false, 'message' => 'Please fill in all required fields.']);
    exit;
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(422);
    echo json_encode(['success' => false, 'message' => 'Please enter a valid email address.']);
    exit;
}

/* ── Build email ────────────────────────────────────── */
$to      = 'info@amrmagdy.com';
$subject = "New CRM Inquiry from {$name} — amrmagdy.com";

$body  = "New message from amrmagdy.com\n";
$body .= str_repeat('─', 50) . "\n\n";
$body .= "Name:    {$name}\n";
$body .= "Email:   {$email}\n";
$body .= "Sent:    " . date('D, d M Y H:i:s T') . "\n\n";
$body .= "Message:\n{$message}\n\n";
$body .= str_repeat('─', 50) . "\n";
$body .= "Reply directly to: {$email}\n";

/*
 * KEY FIX: From address MUST be a real mailbox on your domain.
 * Using info@amrmagdy.com (your actual mailbox) instead of no-reply@.
 * The Reply-To is set to the visitor's email so your replies go to them.
 */
$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "From: amrmagdy.com Contact <info@amrmagdy.com>\r\n";
$headers .= "Reply-To: {$name} <{$email}>\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";
$headers .= "X-Priority: 1\r\n";

/*
 * -f sets the envelope sender (required by many shared hosts).
 * Must also be a real mailbox on your domain.
 */
$extra_params = '-f info@amrmagdy.com';

/* ── Also set sendmail_from for Windows/IIS hosts ───── */
@ini_set('sendmail_from', 'info@amrmagdy.com');

/* ── Send ────────────────────────────────────────────── */
$sent = @mail($to, $subject, $body, $headers, $extra_params);

if ($sent) {
    $_SESSION['last_contact'] = $now;
    echo json_encode(['success' => true, 'message' => 'Message sent!']);
} else {
    /* Log failure with full error detail */
    $phpError  = error_get_last();
    $logEntry  = date('Y-m-d H:i:s') . " | MAIL FAILED";
    $logEntry .= " | from={$email} | name={$name}";
    $logEntry .= " | error=" . ($phpError['message'] ?? 'none') . "\n";
    @file_put_contents(__DIR__ . '/contact_log.txt', $logEntry, FILE_APPEND | LOCK_EX);

    http_response_code(500);
    echo json_encode([
        'success'  => false,
        'message'  => 'The mail server could not deliver your message. Please email info@AmrMagdy.com directly or reach out on WhatsApp at +20 103 327 5250.',
        'mailto'   => true,
    ]);
}
exit;
