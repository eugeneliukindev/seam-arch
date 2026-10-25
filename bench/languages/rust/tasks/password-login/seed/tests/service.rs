use accounts::app::build_service;

#[test]
fn unknown_email_has_no_account() {
    assert!(build_service().find("nobody@example.com").is_none());
}
