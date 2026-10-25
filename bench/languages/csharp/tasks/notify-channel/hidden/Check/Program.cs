using Alerts;

// Hidden checks: one PASS or FAIL line per scenario, read by test_hidden.py.
static void Check(string scenario, Func<bool> passes)
{
    try
    {
        Console.WriteLine($"{(passes() ? "PASS" : "FAIL")} {scenario}");
    }
    catch (Exception error)
    {
        Console.WriteLine($"FAIL {scenario}: {error.GetType().Name}: {error.Message}");
    }
}

Check("sms user gets a text", () =>
{
    var (smtp, sms) = (new FakeSmtp(), new FakeSms());
    App.BuildService(smtp, sms).Alert(new User(1, "a@example.com", "+100") { Channel = Channel.Sms }, "disk full");
    return sms.Sent.SequenceEqual(["+100"]) && smtp.Sent.Count == 0;
});
Check("email user gets mail", () =>
{
    var (smtp, sms) = (new FakeSmtp(), new FakeSms());
    App.BuildService(smtp, sms).Alert(new User(2, "b@example.com", "+200") { Channel = Channel.Email }, "disk full");
    return smtp.Sent.SequenceEqual(["b@example.com"]) && sms.Sent.Count == 0;
});

sealed class FakeSmtp : SmtpClient
{
    public List<string> Sent { get; } = [];

    public override void SendMail(string to, string subject, string body) => Sent.Add(to);
}

sealed class FakeSms : SmsGateway
{
    public List<string> Sent { get; } = [];

    public override void Send(string phone, string text) => Sent.Add(phone);
}
