//! The `invoices` command.

use std::io::{self, Write};

use crate::date::Date;
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
            let mut invoices = store.all();
            invoices.sort_by_key(|invoice| invoice.due);
            for invoice in invoices {
                if invoice.paid || invoice.due >= today {
                    continue;
                }
                let days = today - invoice.due;
                writeln!(out, "{} due {} {:.2} {days} days overdue", invoice.number, invoice.due, invoice.amount)?;
            }
        }
        [unknown, ..] => {
            return Err(io::Error::new(io::ErrorKind::InvalidInput, format!("unknown option {unknown}")));
        }
    }
    Ok(())
}
