//! The `invoices` command.

use std::io::{self, Write};

use crate::date::Date;
use crate::overdue::overdue;
use crate::store::InvoiceStore;

/// Print the invoices, one per line; with `--overdue`, only the late ones.
pub fn run(args: &[&str], store: &dyn InvoiceStore, today: Date, out: &mut dyn Write) -> io::Result<()> {
    match args {
        [] => {
            for invoice in store.all() {
                let status = if invoice.paid { "paid" } else { "open" };
                writeln!(out, "{} due {} {:.2} {}", invoice.number, invoice.due, invoice.amount, status)?;
            }
        }
        ["--overdue"] => {
            for late in overdue(store.all(), today) {
                let invoice = late.invoice;
                writeln!(out, "{} due {} {:.2} {} days overdue", invoice.number, invoice.due, invoice.amount, late.days)?;
            }
        }
        [unknown, ..] => {
            return Err(io::Error::new(io::ErrorKind::InvalidInput, format!("unknown option {unknown}")));
        }
    }
    Ok(())
}
