use accounts::app::build_service;

#[test]
#[allow(unused_mut)]
fn right_password_logs_in() {
    let mut service = build_service();
    let _ = service.register("a@example.com", "s3cret");
    assert!(service.log_in("a@example.com", "s3cret"));
}
