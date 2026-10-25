using Shop;

var failures = 0;

void Check(string test, bool passed)
{
    Console.WriteLine($"{(passed ? "ok  " : "FAIL")} {test}");
    failures += passed ? 0 : 1;
}

Check("cart", new Cart(10m).Total == 10m);

return failures == 0 ? 0 : 1;
