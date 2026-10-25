using Shop;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

Check("order", new Order(1, 9.99m, "EUR").Total == 9.99m);

return failures == 0 ? 0 : 1;
