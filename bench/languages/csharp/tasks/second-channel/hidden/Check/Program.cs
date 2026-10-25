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

// how many messages each gateway got, in the order mail, text, push
static int[] Deliver(User user)
{
    var (smtp, sms, push) = (new FakeSmtp(), new FakeSms(), new FakePush());
    App.BuildService(smtp, sms, push).Alert(user, "disk full");
    return [smtp.Sent.Count, sms.Sent.Count, push.Sent.Count];
}

static User Choosing(Channel channel) => new(1, "a@example.com", "+100", "dev-1") { Channel = channel };

Check("email user gets mail", () => Deliver(Choosing(Channel.Email)).SequenceEqual([1, 0, 0]));
Check("sms user gets a text", () => Deliver(Choosing(Channel.Sms)).SequenceEqual([0, 1, 0]));
Check("push user gets a notification", () => Deliver(Choosing(Channel.Push)).SequenceEqual([0, 0, 1]));

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

sealed class FakePush : PushGateway
{
    public List<string> Sent { get; } = [];

    public override void Send(string deviceToken, string text) => Sent.Add(deviceToken);
}
