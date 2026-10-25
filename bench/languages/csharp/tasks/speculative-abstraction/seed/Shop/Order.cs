namespace Shop;

/// <summary>An order waiting for payment.</summary>
public sealed record Order(int Id, decimal Total, string Currency);
