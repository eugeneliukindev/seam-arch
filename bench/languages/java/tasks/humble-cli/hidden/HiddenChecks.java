import invoices.Cli;
import invoices.Invoice;
import invoices.InvoiceStore;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.Executable;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.RecordComponent;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public final class HiddenChecks {
    static final LocalDate TODAY = LocalDate.of(2026, 10, 1);
    static final List<Invoice> INVOICES = List.of(
        new Invoice("N-3", LocalDate.of(2026, 9, 21), false, new BigDecimal("300.00")),
        new Invoice("N-1", LocalDate.of(2026, 7, 3), false, new BigDecimal("120.00")),
        new Invoice("N-2", LocalDate.of(2026, 8, 25), true, new BigDecimal("80.00")),
        new Invoice("N-4", LocalDate.of(2026, 10, 1), false, new BigDecimal("60.00")),
        new Invoice("N-5", LocalDate.of(2026, 11, 15), false, new BigDecimal("90.00")),
        new Invoice("N-6", LocalDate.of(2026, 9, 2), false, new BigDecimal("45.25")));
    /** Oldest first, with days overdue. */
    static final List<String> EXPECTED = List.of("N-1", "N-6", "N-3");
    static final List<Integer> DAYS = List.of(90, 29, 10);
    static final InvoiceStore STORE = () -> new ArrayList<>(INVOICES);
    static final Pattern NUMBER = Pattern.compile("N-\\d+");

    public static void main(String[] args) throws Exception {
        switch (args[0]) {
            case "overdue" -> {
                String printed = run("--overdue");
                Set<String> numbers = INVOICES.stream().map(Invoice::number).collect(Collectors.toSet());
                List<String> lines = printed.lines().filter(line -> numbersIn(line).stream().anyMatch(numbers::contains)).toList();
                List<String> listed = lines.stream().map(line -> numbersIn(line).get(0)).toList();
                expect(listed.equals(EXPECTED), "listed " + listed + " in\n" + printed);
                for (int i = 0; i < lines.size(); i++) {
                    Pattern days = Pattern.compile("(?<![\\d.-])" + DAYS.get(i) + "(?![\\d.-])");
                    expect(days.matcher(lines.get(i)).find(), "no " + DAYS.get(i) + " days in " + lines.get(i));
                }
            }
            case "plain" -> {
                String printed = run();
                expect(INVOICES.stream().allMatch(invoice -> printed.contains(invoice.number())), "listed\n" + printed);
            }
            case "decides" -> {
                List<String> tried = new ArrayList<>();
                for (String name : Arrays.copyOfRange(args, 1, args.length)) {
                    Class<?> type = Class.forName(name);
                    for (Method method : type.getDeclaredMethods()) {
                        if (!method.isSynthetic() && method.getReturnType() != void.class) {
                            tried.add(type.getSimpleName() + "." + method.getName());
                            if (returnsOverdue(type, method)) {
                                return;
                            }
                        }
                    }
                }
                throw new AssertionError("no method outside Cli.java returns the overdue invoices; tried " + tried);
            }
            default -> throw new IllegalArgumentException(args[0]);
        }
    }

    private static String run(String... args) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        Cli.run(args, STORE, TODAY, new PrintStream(out, true, StandardCharsets.UTF_8));
        return out.toString(StandardCharsets.UTF_8);
    }

    private static List<String> numbersIn(String line) {
        List<String> found = new ArrayList<>();
        Matcher matcher = NUMBER.matcher(line);
        while (matcher.find()) {
            found.add(matcher.group());
        }
        return found;
    }

    /** Whether {@code method}, given the invoices and today in any form it asks for, returns the overdue ones and prints nothing. */
    private static boolean returnsOverdue(Class<?> type, Method method) {
        PrintStream stdout = System.out;
        ByteArrayOutputStream printed = new ByteArrayOutputStream();
        try {
            Optional<Object[]> arguments = argumentsFor(method);
            Optional<Object> receiver = Modifier.isStatic(method.getModifiers()) ? Optional.of(type) : receiverOf(type);
            if (arguments.isEmpty() || receiver.isEmpty()) {
                return false;
            }
            method.setAccessible(true);
            System.setOut(new PrintStream(printed, true, StandardCharsets.UTF_8));
            Object result = method.invoke(Modifier.isStatic(method.getModifiers()) ? null : receiver.get(), arguments.get());
            System.setOut(stdout);
            List<String> found = invoicesIn(result).stream().map(Invoice::number).sorted().toList();
            return !found.isEmpty() && found.equals(EXPECTED.stream().sorted().toList()) && printed.size() == 0;
        } catch (ReflectiveOperationException | RuntimeException refused) {
            return false;
        } finally {
            System.setOut(stdout);
        }
    }

    private static Optional<Object> receiverOf(Class<?> type) throws ReflectiveOperationException {
        if (type.isInstance(STORE)) {
            return Optional.of(STORE);
        }
        if (type.isInterface() || Modifier.isAbstract(type.getModifiers())) {
            return Optional.empty();
        }
        for (Constructor<?> constructor : type.getDeclaredConstructors()) {
            Optional<Object[]> arguments = argumentsFor(constructor);
            if (arguments.isPresent()) {
                constructor.setAccessible(true);
                return Optional.of(constructor.newInstance(arguments.get()));
            }
        }
        return Optional.empty();
    }

    private static Optional<Object[]> argumentsFor(Executable executable) {
        List<Object> arguments = new ArrayList<>();
        for (Class<?> parameter : executable.getParameterTypes()) {
            Optional<Object> value = valueFor(parameter);
            if (value.isEmpty()) {
                return Optional.empty();
            }
            arguments.add(value.get());
        }
        return Optional.of(arguments.toArray());
    }

    /** The invoices, today or the store, in the form {@code parameter} asks for. */
    private static Optional<Object> valueFor(Class<?> parameter) {
        if (parameter == LocalDate.class) {
            return Optional.of(TODAY);
        }
        if (parameter == Clock.class) {
            return Optional.of(Clock.fixed(TODAY.atStartOfDay(ZoneOffset.UTC).toInstant(), ZoneOffset.UTC));
        }
        if (parameter == Stream.class) {
            return Optional.of(INVOICES.stream());
        }
        if (parameter == Invoice[].class) {
            return Optional.of(INVOICES.toArray(Invoice[]::new));
        }
        if (parameter != Object.class && parameter.isAssignableFrom(ArrayList.class)) {
            return Optional.of(new ArrayList<>(INVOICES));
        }
        if (parameter != Object.class && parameter.isInstance(STORE)) {
            return Optional.of(STORE);
        }
        return Optional.empty();
    }

    private static List<Invoice> invoicesIn(Object result) throws ReflectiveOperationException {
        List<Object> items = new ArrayList<>();
        switch (result) {
            case null -> { }
            case Map<?, ?> map -> {
                items.addAll(map.keySet());
                items.addAll(map.values());
            }
            case Collection<?> collection -> items.addAll(collection);
            case Iterable<?> iterable -> iterable.forEach(items::add);
            case Stream<?> stream -> items.addAll(stream.toList());
            case Object[] array -> items.addAll(Arrays.asList(array));
            default -> { }
        }
        List<Invoice> found = new ArrayList<>();
        for (Object item : items) {
            found.addAll(invoicesOf(item));
        }
        return found;
    }

    private static List<Invoice> invoicesOf(Object item) throws ReflectiveOperationException {
        if (item instanceof Invoice invoice) {
            return List.of(invoice);
        }
        if (item == null) {
            return List.of();
        }
        List<Object> values = new ArrayList<>();
        if (item instanceof Map.Entry<?, ?> entry) {
            values.add(entry.getKey());
            values.add(entry.getValue());
        } else if (item.getClass().isRecord()) {
            for (RecordComponent component : item.getClass().getRecordComponents()) {
                Method accessor = component.getAccessor();
                accessor.setAccessible(true);
                values.add(accessor.invoke(item));
            }
        } else {
            for (Class<?> type = item.getClass(); type != null && type != Object.class; type = type.getSuperclass()) {
                for (Field field : type.getDeclaredFields()) {
                    if (!Modifier.isStatic(field.getModifiers()) && field.trySetAccessible()) {
                        values.add(field.get(item));
                    }
                }
            }
        }
        return values.stream().filter(Invoice.class::isInstance).map(Invoice.class::cast).toList();
    }

    private static void expect(boolean passed, String message) {
        if (!passed) {
            throw new AssertionError(message);
        }
    }
}
