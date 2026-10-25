<p align="center">
  <img src="../assets/hero.png" width="880" alt="seam-arch: 31 de 35 comprobaciones de diseño frente a 8 sin él, en seis lenguajes; todas las comprobaciones de comportamiento pasan.">
</p>

<p align="center">
  <em>Decide dónde va el código, y nada acaba en el sitio equivocado.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/one%20file-379%20words-111111?style=flat-square" alt="Un archivo, 379 palabras">
  <img src="https://img.shields.io/badge/built%20on-Clean%20Architecture-111111?style=flat-square" alt="Basado en Clean Architecture">
  <img src="https://img.shields.io/badge/measured-6%20languages-111111?style=flat-square" alt="Medido en seis lenguajes">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="Licencia MIT">
</p>

<p align="center">
  <a href="#ejemplos">Ejemplos</a> &middot;
  <a href="#cifras">Cifras</a> &middot;
  <a href="#instalación">Instalación</a> &middot;
  <a href="#tareas">Tareas</a> &middot;
  <a href="#fuentes">Fuentes</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.ru.md">Русский</a> &middot; <strong>Español</strong> &middot; <a href="README.ko.md">한국어</a> &middot; <a href="README.zh-CN.md">简体中文</a> &middot; <a href="README.ja.md">日本語</a></sub>
</p>

---

**seam-arch** es un único `AGENTS.md` que enseña arquitectura a un agente de código: dónde va el código y cómo dependen sus partes unas de otras. Lo guía una sola pregunta: *hecho de otra forma, ¿decidiría el programa algo distinto?* Si no, es un detalle, y llega a la lógica de negocio solo a través de un tipo que un test pueda sustituir.

> [!NOTE]
> Basado en *Clean Architecture* de Robert C. Martin: la Regla de Dependencia, SOLID, Humble Object, datos simples a través de las fronteras. Cada regla se ganó su línea en una tarea que los agentes fallan sin ella.

## Ejemplos

Salida real del benchmark, recortada. La imagen es la vista previa; abre un lenguaje debajo para ver el código que escribió el agente.

### 1. Alertas: SOLID en un servicio

**"Los usuarios pueden elegir SMS en vez de email; sin teléfono, email. Después: push."** Python, tres ejecuciones: sin AGENTS.md 0/3, con él 3/3.

<p align="center">
  <img src="../assets/case-alerts.png" width="880" alt="Sin seam-arch el servicio ramifica según el canal. Con seam-arch, un contrato Notifier, cada canal en su propia clase con su propio respaldo, elegido en el punto de entrada.">
</p>

<details>
<summary><strong>Python</strong></summary>

```python
class Notifier(Protocol):
    def notify(self, user: User, text: str) -> None: ...

class AlertService:
    def __init__(self, notifiers: Mapping[Channel, Notifier]) -> None:
        self._notifiers = notifiers
    def alert(self, user, text):
        self._notifiers[user.channel].notify(user, text)

# app.py
return AlertService({"email": EmailNotifier(smtp), "sms": SmsNotifier(sms)})
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```ts
export interface Notifier {
  notify(user: User, text: string): void;
}

export class AlertService {
  constructor(private readonly notifiers: Readonly<Record<Channel, Notifier>>) {}
  alert(user: User, text: string): void {
    this.notifiers[user.channel].notify(user, text);
  }
}

// app.ts
return new AlertService({ email: new EmailNotifier(smtp), sms: new SmsNotifier(sms) });
```
</details>

<details>
<summary><strong>Go</strong></summary>

```go
type Notifier interface {
	Notify(user User, text string) error
}

func (s *AlertService) Alert(user User, text string) error {
	n, ok := s.notifiers[user.Channel]
	if !ok {
		return fmt.Errorf("%w: %q", ErrUnknownChannel, user.Channel)
	}
	return n.Notify(user, text)
}

// app.go
return NewAlertService(map[string]Notifier{"email": email, "sms": NewSmsNotifier(sms)})
```
</details>

<details>
<summary><strong>Java</strong></summary>

```java
public interface Notifier {
    void deliver(User user, String text);
}

public AlertService(Map<Channel, Notifier> notifiers) { this.notifiers = Map.copyOf(notifiers); }

public void alert(User user, String text) {
    notifiers.get(user.channel()).deliver(user, text);
}

// App.java
return new AlertService(Map.of(Channel.EMAIL, new EmailNotifier(smtp), Channel.SMS, new SmsNotifier(sms)));
```
</details>

<details>
<summary><strong>C#</strong></summary>

```csharp
public interface INotifier
{
    void Notify(User user, string text);
}

public sealed class AlertService(IReadOnlyDictionary<Channel, INotifier> notifiers)
{
    public void Alert(User user, string text) => notifiers[user.Channel].Notify(user, text);
}

// App.cs
new Dictionary<Channel, INotifier> { [Channel.Email] = new EmailNotifier(smtp), [Channel.Sms] = new SmsNotifier(sms) }
```
</details>

<details>
<summary><strong>Rust</strong></summary>

```rust
pub trait Notifier {
    fn notify(&self, user: &User, text: &str) -> Result<(), NotifyError>;
}

pub struct AlertService {
    notifiers: HashMap<Channel, Rc<dyn Notifier>>,
}

// app.rs
notifiers.insert(Channel::Email, Rc::new(EmailNotifier::new(smtp)));
notifiers.insert(Channel::Sms, Rc::new(SmsNotifier::new(sms)));
AlertService::new(notifiers)
```
</details>

### 2. Checkout: una costura solo donde hace falta

**"Cupón con caducidad, IVA por país, cobro con Stripe. Quizá PayPal más adelante."** Python, tres ejecuciones: sin AGENTS.md 0/3, con él 3/3. La tarea más difícil: en los demás lenguajes el agente sigue envolviendo Stripe en cuatro de cinco.

<p align="center">
  <img src="../assets/case-checkout.png" width="880" alt="Sin seam-arch, un envoltorio PaymentGateway que nadie necesita y el reloj leído dentro. Con seam-arch el tiempo llega desde fuera, el IVA es una tabla y se usa la propia clase de Stripe.">
</p>

<details>
<summary><strong>Python</strong></summary>

```python
class Checkout:
    def __init__(self, *, coupons: CouponBook, vat_rates: Mapping[str, float], client: StripeClient) -> None:
        self._coupons = coupons
        self._vat_rates = vat_rates
        self._client = client

    def pay(self, cart: Cart, code: str, country: str, card_token: str) -> str:
        coupon = self._coupons.redeem(code)          # refuses an expired coupon, on the injected clock
        discounted = cart.total * (100 - coupon.percent) / 100
        total = discounted * (1 + self._vat_rates.get(country, 0.0))
        return self._client.create_charge(amount_cents=round(total * 100), currency="eur", source=card_token)

# app.py
VAT_RATES = {"GB": 0.20, "DE": 0.19, "NL": 0.21}

def build_checkout(client: StripeClient) -> Checkout:
    coupons = CouponBook(now=lambda: datetime.now(UTC))
    return Checkout(coupons=coupons, vat_rates=VAT_RATES, client=client)
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```ts
export function amountDue(totalCents: number, couponPercent: number, country: string): number {
  const discounted = Math.round((totalCents * (100 - couponPercent)) / 100);
  return discounted + Math.round((discounted * (VAT_PERCENT[country] ?? 0)) / 100);
}

export class Checkout {
  constructor(
    private readonly coupons: CouponBook,
    private readonly client: StripeClient,
    private readonly now: () => Date,
  ) {}
  async pay(cart: Cart, code: string, country: string, cardToken: string): Promise<string> {
    const coupon = redeem(this.coupons, code, this.now());
    const amountCents = amountDue(Math.round(cart.total * 100), coupon.percent, country);
    return this.client.createCharge({ amountCents, currency: "EUR", source: cardToken });
  }
}

// app.ts
return new Checkout(new CouponBook(), client, () => new Date());
```
</details>

<details>
<summary><strong>Go</strong></summary>

```go
type Checkout struct {
	Coupons    *CouponBook
	Charger    Charger // StripeClient is one
	VATPercent map[string]int64
	Now        func() time.Time
}

func (c *Checkout) Pay(ctx context.Context, cart Cart, code, country, cardToken string) (string, error) {
	total := cart.TotalCents
	if code != "" {
		percent, err := c.Coupons.Redeem(code, c.Now())
		if err != nil {
			return "", err
		}
		total -= total * percent / 100
	}
	total += (total*c.VATPercent[country] + 50) / 100
	return c.Charger.CreateCharge(ctx, total, "EUR", cardToken)
}

// app.go
return &Checkout{Coupons: NewCouponBook(), Charger: client,
	VATPercent: map[string]int64{"GB": 20, "DE": 19, "NL": 21}, Now: time.Now}
```
</details>

<details>
<summary><strong>Java</strong></summary>

```java
public Checkout(CouponBook coupons, VatRates vat, StripeClient client, Clock clock) { ... }

public String pay(Cart cart, String code, String country, String cardToken) {
    Coupon coupon = coupons.find(code);
    if (!clock.instant().isBefore(coupon.expires())) {
        throw new CouponExpiredException(code);
    }
    long cents = priceInCents(cart.total(), coupon.percent(), vat.rateFor(country));
    return client.createCharge(cents, "eur", cardToken);
}

// App.java
VatRates vat = new VatRates(Map.of("GB", new BigDecimal("0.20"), "DE", new BigDecimal("0.19"), "NL", new BigDecimal("0.21")));
return new Checkout(new CouponBook(), vat, client, Clock.systemUTC());
```
</details>

<details>
<summary><strong>C#</strong></summary>

```csharp
public sealed class Checkout(
    CouponBook coupons,
    IReadOnlyDictionary<string, decimal> vatRates,
    StripeClient client,
    Func<DateTimeOffset> now)
{
    public string Pay(Cart cart, string code, string country, string cardToken)
    {
        var coupon = coupons.Find(code);
        if (coupon.Expires < now()) throw new CouponExpiredException(code);
        var vat = vatRates.GetValueOrDefault(country, 0m);
        return client.CreateCharge(Cents(cart.Total, coupon.Percent, vat), "eur", cardToken);
    }
}

// App.cs
new Checkout(new CouponBook(), VatRates, client, () => DateTimeOffset.UtcNow);
```
</details>

<details>
<summary><strong>Rust</strong></summary>

```rust
pub struct Checkout {
    pub coupons: CouponBook,
    client: Box<dyn StripeClient>,
    now: Box<dyn Fn() -> SystemTime>,
}

impl Checkout {
    pub fn pay(&self, cart: &Cart, code: &str, country: &str, card_token: &str) -> Result<String, CheckoutError> {
        let coupon = self.coupons.redeem(code, (self.now)())?;
        let amount = price_cents(cart.total_cents, coupon.percent, vat_percent(country));
        Ok(self.client.create_charge(amount, "EUR", card_token))
    }
}

// vat.rs
pub fn vat_percent(country: &str) -> u64 {
    match country { "GB" => 20, "DE" => 19, "NL" => 21, _ => 0 }
}

// app.rs
Checkout::new(client, Box::new(SystemTime::now))
```
</details>

El tiempo decide, así que llega desde fuera. El IVA son datos, así que sigue siendo una tabla. La clase de Stripe ya se puede simular, así que no lleva envoltorio.

### 3. Contraseñas: un detalle tras un contrato

**"Las cuentas necesitan contraseñas. Hash con scrypt y una sal aleatoria."** Sin AGENTS.md 0/6 lenguajes, con él 6/6.

<p align="center">
  <img src="../assets/case-password.png" width="880" alt="Sin seam-arch el servicio importa hashlib y ejecuta scrypt él mismo. Con seam-arch, un contrato PasswordHasher, el servicio lo llama y el punto de entrada elige ScryptHasher.">
</p>

<details>
<summary><strong>Python</strong></summary>

```python
class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> bytes: ...
    @abstractmethod
    def verify(self, password: str, password_hash: bytes) -> bool: ...

class AccountService:
    def __init__(self, *, users: UserStore, hasher: PasswordHasher) -> None:
        self._users = users
        self._hasher = hasher

    def log_in(self, email: str, password: str) -> bool:
        user = self._users.find(email)
        if user is None or not user.password_hash:
            return False
        return self._hasher.verify(password, user.password_hash)

# app.py
return AccountService(users=InMemoryUsers(), hasher=ScryptHasher())
```
</details>

<details>
<summary><strong>TypeScript</strong></summary>

```ts
export interface PasswordHasher {
  hash(password: string): string;
  verify(password: string, hash: string): boolean;
}

export class AccountService {
  constructor(
    private readonly users: UserStore,
    private readonly hasher: PasswordHasher,
  ) {}
  logIn(email: string, password: string): boolean {
    const user = this.users.find(email);
    return user !== undefined && this.hasher.verify(password, user.passwordHash);
  }
}

// app.ts
return new AccountService(new InMemoryUsers(), new ScryptHasher());
```
</details>

<details>
<summary><strong>Go</strong></summary>

```go
type PasswordHasher interface {
	Hash(password string) ([]byte, error)
	Matches(hash []byte, password string) bool
}

func NewAccountService(users UserStore, hasher PasswordHasher) *AccountService {
	return &AccountService{users: users, hasher: hasher}
}

func (s *AccountService) LogIn(email, password string) (bool, error) {
	user, ok := s.users.Find(email)
	if !ok {
		return false, nil
	}
	return s.hasher.Matches(user.PasswordHash, password), nil
}

// app.go
return NewAccountService(NewInMemoryUsers(), PBKDF2Hasher{})
```
</details>

<details>
<summary><strong>Java</strong></summary>

```java
public interface PasswordHasher {
    byte[] hash(String password);
    boolean matches(String password, byte[] stored);
}

public AccountService(UserStore users, PasswordHasher hasher) {
    this.users = users;
    this.hasher = hasher;
}

public boolean logIn(String email, String password) {
    return users.find(email)
            .filter(user -> user.passwordHash().length > 0)
            .map(user -> hasher.matches(password, user.passwordHash()))
            .orElse(false);
}

// App.java
return new AccountService(new InMemoryUsers(), new Pbkdf2PasswordHasher());
```
</details>

<details>
<summary><strong>C#</strong></summary>

```csharp
public interface IPasswordHasher
{
    byte[] Hash(string password);
    bool Verify(string password, byte[] stored);
}

public sealed class AccountService(IUserStore users, IPasswordHasher hasher)
{
    public bool LogIn(string email, string password) =>
        users.Find(email) is { } user && hasher.Verify(password, user.PasswordHash);
}

// App.cs
public static AccountService BuildService() => new(new InMemoryUsers(), new Pbkdf2PasswordHasher());
```
</details>

<details>
<summary><strong>Rust</strong></summary>

```rust
pub trait PasswordHasher {
    fn new_salt(&self) -> Vec<u8>;
    fn derive(&self, password: &str, salt: &[u8]) -> Vec<u8>;
}

pub struct AccountService {
    users: Box<dyn UserStore>,
    hasher: Box<dyn PasswordHasher>,
}

// app.rs
AccountService::new(Box::new(InMemoryUsers::default()), Box::new(KdfHasher))
```
</details>

El servicio decide quién inicia sesión; cómo se hashean los bytes es un detalle, aunque la tarea lo nombre y la biblioteca estándar lo tenga.

## Cifras

El mismo agente con y sin AGENTS.md.

| lenguaje | tareas de diseño | sin AGENTS.md | con AGENTS.md |
|---|:-:|:-:|:-:|
| Python | 10 | 2/10 | **10/10** |
| TypeScript | 5 | 1/5 | **4/5** |
| Go | 5 | 1/5 | **4/5** |
| Java | 5 | 2/5 | **4/5** |
| C# | 5 | 1/5 | **5/5** |
| Rust | 5 | 1/5 | **4/5** |

Todos los lenguajes tienen las mismas diez tareas; fuera de Python, de momento se miden cinco. `speculative-abstraction` es el contrapeso: falla si las reglas sobrediseñan. Todas las comprobaciones de comportamiento pasan en ambos brazos: seam-arch cambia dónde va el código, no si funciona.

## Instalación

`AGENTS.md` es el único archivo. Guarda una copia y enlázala allí donde tus agentes leen sus reglas:

```bash
curl -fsSL --create-dirs -o ~/seam-arch/AGENTS.md https://raw.githubusercontent.com/eugeneliukindev/seam-arch/main/AGENTS.md

mkdir -p ~/.claude/rules && ln -s ~/seam-arch/AGENTS.md ~/.claude/rules/seam-arch.md   # Claude Code
ln -s ~/seam-arch/AGENTS.md ~/.codex/AGENTS.md                                       # Codex
ln -s ~/seam-arch/AGENTS.md ~/.gemini/GEMINI.md                                      # Gemini CLI
ln -s ~/seam-arch/AGENTS.md ~/.config/opencode/AGENTS.md                             # opencode
ln -s ~/seam-arch/AGENTS.md ./AGENTS.md          # one project: Cursor, Copilot, Zed and any agent that reads AGENTS.md
```

Vuelve a ejecutar el mismo `curl` para actualizar todos los agentes a la vez.

## Tareas

Cada tarea es un ticket corriente en un repositorio pequeño; una comprobación oculta, que el agente nunca ve, examina el diseño. Un número indica cuántos lenguajes pasaron; ✗ y ✓ son Python, donde los demás lenguajes aún no se miden.

| tarea | qué se pide al agente | qué busca la comprobación oculta | sin AGENTS.md | con AGENTS.md |
|---|---|---|:-:|:-:|
| `heavy-decision` | resumir un currículum: leer el archivo, ponerle nota | DIP: el lector de archivos llega como parámetro | 0/6 | 6/6 |
| `notify-channel` | los usuarios pueden elegir SMS en vez de email | OCP: un canal nuevo es una clase nueva, no una rama | 1/6 | 6/6 |
| `password-login` | añadir login, hash con scrypt | DIP: el hash tras un contrato, no en el servicio | 0/6 | 6/6 |
| `combo-checkout` | cupón con caducidad, IVA por país, cobro con Stripe | una costura solo donde hace falta: tiempo desde fuera, IVA como datos, sin envoltorio para Stripe | 1/6 | 2/6 |
| `combo-alerts` | SMS con respaldo por email, luego push en una segunda sesión | SOLID: sin ramas por canal, contrato de un método, todos los notificadores lo cumplen | ✗ | ✓ |
| `coupon-expiry` | rechazar cupones caducados | DIP: el reloj llega desde fuera | ✗ | ✓ |
| `humble-cli` | añadir --overdue a una CLI | Humble Object: la CLI solo parsea e imprime | ✗ | ✓ |
| `plain-records` | consejo de paraguas a partir de una API de previsión | frontera: la respuesta cruda se convierte en registro en el borde | ✗ | ✓ |
| `second-channel` | SMS, luego push en una segunda sesión | OCP tras dos ediciones | ✗ | ✓ |
| `speculative-abstraction` | cobrar con Stripe, "quizá PayPal más adelante" | el contrapeso: sin interfaz para el único cliente | 6/6 | 6/6 |

## Fuentes

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) y *Clean Architecture*: la Regla de Dependencia, SOLID, Humble Object, fronteras.
- Michael Feathers, *Working Effectively with Legacy Code*: costuras.
- Miško Hevery, [Guide: Writing Testable Code](https://github.com/mhevery/guide-to-testable-code): pide los colaboradores, nunca los busques.
- Robert C. Martin, *Clean Code*: argumentos bandera, envolver APIs de terceros.
- [Guías de estilo de Google](https://google.github.io/styleguide/cppguide.html#Parting_Words): sigue el código que te rodea.
- Alexis King, [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/): valida en la frontera.

## Licencia

[MIT](../LICENSE).
