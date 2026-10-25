using System.Collections;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using Invoices;

// Hidden checks: one PASS or FAIL line per scenario, read by test_hidden.py.
// The arguments name the types declared in Invoices/Cli.cs, which cannot be what decides.
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

var today = new DateOnly(2026, 10, 1);
Invoice[] invoices =
[
    new("N-3", new DateOnly(2026, 9, 21), false, 300.0m),
    new("N-1", new DateOnly(2026, 7, 3), false, 120.0m),
    new("N-2", new DateOnly(2026, 8, 25), true, 80.0m),
    new("N-4", new DateOnly(2026, 10, 1), false, 60.0m),
    new("N-5", new DateOnly(2026, 11, 15), false, 90.0m),
    new("N-6", new DateOnly(2026, 9, 2), false, 45.25m),
];
// oldest first, with days overdue
(string Number, int Days)[] expected = [("N-1", 90), ("N-6", 29), ("N-3", 10)];
var store = new Store(invoices);
var numbers = invoices.Select(invoice => invoice.Number).ToHashSet();

string Printed(string[] arguments)
{
    var output = new StringWriter();
    Cli.Run(arguments, store, today, output);
    return output.ToString();
}

Check("overdue lists late invoices oldest first", () =>
{
    var lines = Printed(["--overdue"]).Split('\n')
        .Where(line => Regex.Matches(line, @"N-\d+").Any(match => numbers.Contains(match.Value)))
        .ToList();
    return lines.Select(line => Regex.Match(line, @"N-\d+").Value).SequenceEqual(expected.Select(late => late.Number))
        && lines.Zip(expected).All(pair => Regex.IsMatch(pair.First, $@"(?<![\d.-]){pair.Second.Days}(?![\d.-])"));
});
Check("plain listing still lists everything", () =>
{
    var printed = Printed([]);
    return numbers.All(printed.Contains);
});

// the argument for one parameter of a candidate, or null when the candidate asks for something else
object? Argument(ParameterInfo parameter)
{
    var type = parameter.ParameterType;
    if (type == typeof(DateOnly))
    {
        return today;
    }
    if (type == typeof(DateTime))
    {
        return today.ToDateTime(TimeOnly.MinValue);
    }
    object[] sources = [invoices.ToList(), invoices.ToArray(), new Store(invoices)];
    return sources.FirstOrDefault(type.IsInstanceOfType);
}

IEnumerable<Invoice> InvoicesIn(object? item) => item switch
{
    Invoice invoice => [invoice],
    ITuple tuple => Enumerable.Range(0, tuple.Length).Select(index => tuple[index]).OfType<Invoice>(),
    null => [],
    _ => item.GetType().GetProperties(BindingFlags.Instance | BindingFlags.Public)
        .Where(property => property.GetIndexParameters().Length == 0)
        .Select(property => property.GetValue(item))
        .Concat(item.GetType().GetFields(BindingFlags.Instance | BindingFlags.Public).Select(field => field.GetValue(item)))
        .OfType<Invoice>(),
};

bool ReturnsOverdue(MethodInfo method)
{
    var parameters = method.GetParameters();
    var arguments = parameters.Select(parameter => Argument(parameter) ?? (parameter.HasDefaultValue ? parameter.DefaultValue : null)).ToArray();
    var given = parameters.Where(parameter => !parameter.HasDefaultValue).Select(Argument).ToList();
    if (given.Count != 2 || given.Any(argument => argument is null) || !given.Any(argument => argument is DateOnly or DateTime))
    {
        return false;
    }
    var target = method.IsStatic ? null : Activator.CreateInstance(method.DeclaringType!, nonPublic: true);
    var console = Console.Out;
    var printed = new StringWriter();
    try
    {
        Console.SetOut(printed);
        if (method.Invoke(target, arguments) is not IEnumerable result || result is string)
        {
            return false;
        }
        var found = result.Cast<object?>().SelectMany(InvoicesIn).Select(invoice => invoice.Number).Order().ToList();
        return found.SequenceEqual(expected.Select(late => late.Number).Order()) && printed.ToString().Length == 0;
    }
    catch (Exception)
    {
        return false;
    }
    finally
    {
        Console.SetOut(console);
    }
}

static bool OutsideTheCommand(Type type, ISet<string> command)
{
    for (var declaring = type; declaring is not null; declaring = declaring.DeclaringType)
    {
        if (command.Contains(declaring.Name) || declaring.Name.Contains('<') || declaring.IsDefined(typeof(CompilerGeneratedAttribute)))
        {
            return false;
        }
    }
    return !type.ContainsGenericParameters;
}

Check("a type outside the command returns the overdue invoices", () =>
{
    var command = args.ToHashSet();
    var flags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance | BindingFlags.DeclaredOnly;
    return typeof(Invoice).Assembly.GetTypes()
        .Where(type => OutsideTheCommand(type, command))
        .SelectMany(type => type.GetMethods(flags))
        .Where(method => !method.ContainsGenericParameters && !method.IsAbstract
            && (method.IsStatic || !method.DeclaringType!.IsAbstract && method.DeclaringType.GetConstructor(Type.EmptyTypes) is not null))
        .Any(ReturnsOverdue);
});

sealed class Store(IReadOnlyList<Invoice> invoices) : IInvoiceStore
{
    public IReadOnlyList<Invoice> All() => invoices;
}
