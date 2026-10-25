use accounts::app::build_service;

#[test]
#[allow(unused_mut)]
fn wrong_password_or_email_fails() {
    let mut service = build_service();
    let _ = service.register("a@example.com", "s3cret");
    assert!(!service.log_in("a@example.com", "guess"));
    assert!(!service.log_in("b@example.com", "s3cret"));
}
