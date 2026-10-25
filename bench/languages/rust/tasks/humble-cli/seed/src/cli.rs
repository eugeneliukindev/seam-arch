//! The `invoices` command.

use std::io::{self, Write};

use crate::date::Date;
use crate::store::InvoiceStore;

/// Print the invoices, one per line.
pub fn run(args: &[&str], store: &dyn InvoiceStore, _today: Date, out: &mut dyn Write) -> io::Result<()> {
    if let Some(unknown) = args.first() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, format!("unknown option {unknown}")));
    }
    for invoice in store.all() {
        let status = if invoice.paid { "paid" } else { "open" };
        writeln!(out, "{} due {} {:.2} {}", invoice.number, invoice.due, invoice.amount, status)?;
    }
    Ok(())
}
