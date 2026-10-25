using Alerts;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

var smtp = new FakeSmtp();
App.BuildService(smtp, new SmsGateway(), new PushGateway()).Alert(new User(1, "a@example.com"), "disk full");
Check("alert by mail", smtp.Sent.SequenceEqual([("a@example.com", "disk full")]));

return failures == 0 ? 0 : 1;

sealed class FakeSmtp : SmtpClient
{
    public List<(string To, string Body)> Sent { get; } = [];

    public override void SendMail(string to, string subject, string body) => Sent.Add((to, body));
}
