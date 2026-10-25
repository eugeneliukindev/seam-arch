<p align="center">
  <img src="../assets/hero.png" width="880" alt="seam-arch: 여섯 언어에서 설계 검사 35개 중 31개, 없을 때는 8개. 동작 검사는 모두 통과.">
</p>

<p align="center">
  <em>코드가 어디에 놓일지 그가 정하고, 엉뚱한 곳에 놓이는 것은 없다.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/one%20file-379%20words-111111?style=flat-square" alt="파일 하나, 379단어">
  <img src="https://img.shields.io/badge/built%20on-Clean%20Architecture-111111?style=flat-square" alt="Clean Architecture 기반">
  <img src="https://img.shields.io/badge/measured-6%20languages-111111?style=flat-square" alt="여섯 언어로 측정">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT 라이선스">
</p>

<p align="center">
  <a href="#예시">예시</a> &middot;
  <a href="#수치">수치</a> &middot;
  <a href="#설치">설치</a> &middot;
  <a href="#과제">과제</a> &middot;
  <a href="#출처">출처</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.ru.md">Русский</a> &middot; <a href="README.es.md">Español</a> &middot; <strong>한국어</strong> &middot; <a href="README.zh-CN.md">简体中文</a> &middot; <a href="README.ja.md">日本語</a></sub>
</p>

---

**seam-arch**는 코딩 에이전트에게 아키텍처를 가르치는 `AGENTS.md` 하나다. 코드가 어디에 놓이고 각 부분이 서로 어떻게 의존하는지를 다룬다. 질문은 하나다. *다른 방식으로 했다면 프로그램이 내리는 결정이 달라지는가?* 달라지지 않는다면 그것은 세부사항이고, 테스트가 바꿔 끼울 수 있는 타입을 통해서만 비즈니스 로직에 닿는다.

> [!NOTE]
> Robert C. Martin의 *Clean Architecture*에 기반한다. 의존성 규칙, SOLID, Humble Object, 경계를 넘는 평범한 데이터. 모든 규칙은 그것 없이는 에이전트가 실패하는 과제에서 자기 자리를 얻었다.

## 예시

벤치마크의 실제 출력을 다듬은 것이다. 그림은 미리보기이고, 그 아래 언어를 펼치면 에이전트가 그 언어로 쓴 코드가 보인다.

### 1. 알림: 서비스 하나 안의 SOLID

**"사용자는 이메일 대신 SMS를 고를 수 있다. 전화번호가 없으면 이메일. 다음은 푸시."** Python, 세 번 실행: AGENTS.md 없이 0/3, 있으면 3/3.

<p align="center">
  <img src="../assets/case-alerts.png" width="880" alt="seam-arch 없이는 서비스가 채널에 따라 분기한다. seam-arch가 있으면 Notifier 계약 하나, 채널마다 자체 대체 경로를 가진 클래스, 진입점에서 선택.">
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

### 2. 결제: 필요한 곳에만 이음새

**"만료일이 있는 쿠폰, 국가별 VAT, Stripe로 결제. 나중에 PayPal도 될지 모름."** Python, 세 번 실행: AGENTS.md 없이 0/3, 있으면 3/3. 가장 어려운 과제다. 다른 언어에서는 다섯 중 넷에서 에이전트가 여전히 Stripe를 감싼다.

<p align="center">
  <img src="../assets/case-checkout.png" width="880" alt="seam-arch 없이는 아무도 필요로 하지 않는 PaymentGateway 래퍼와 안에서 읽는 시계. seam-arch가 있으면 시간은 밖에서 들어오고, VAT는 표이고, Stripe 자체 클래스를 쓴다.">
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

시간은 결정을 바꾸므로 밖에서 들어온다. VAT는 데이터이므로 표로 남는다. Stripe 클래스는 이미 가짜로 바꿀 수 있으므로 래퍼가 없다.

### 3. 비밀번호: 계약 뒤의 세부사항

**"계정에는 비밀번호가 필요하다. scrypt와 무작위 솔트로 해시하라."** AGENTS.md 없이 0/6 언어, 있으면 6/6.

<p align="center">
  <img src="../assets/case-password.png" width="880" alt="seam-arch 없이는 서비스가 hashlib을 import하고 scrypt를 직접 실행한다. seam-arch가 있으면 PasswordHasher 계약, 서비스는 그것을 호출하고, 진입점이 ScryptHasher를 고른다.">
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

누가 로그인하는지는 서비스가 정한다. 바이트를 어떻게 해시하는지는 세부사항이다. 과제가 그 방법을 지정하고 표준 라이브러리에 있더라도 마찬가지다.

## 수치

같은 에이전트를 AGENTS.md 없이와 있이 실행.

| 언어 | 설계 과제 | AGENTS.md 없이 | AGENTS.md 있이 |
|---|:-:|:-:|:-:|
| Python | 10 | 2/10 | **10/10** |
| TypeScript | 5 | 1/5 | **4/5** |
| Go | 5 | 1/5 | **4/5** |
| Java | 5 | 2/5 | **4/5** |
| C# | 5 | 1/5 | **5/5** |
| Rust | 5 | 1/5 | **4/5** |

모든 언어에 같은 과제 열 개가 있다. Python 밖에서는 지금까지 그중 다섯 개만 측정했다. `speculative-abstraction`은 균형추다. 규칙이 과잉 설계하면 실패한다. 동작 검사는 양쪽 모두 전부 통과한다. seam-arch가 바꾸는 것은 코드가 놓이는 곳이지, 코드가 동작하는지가 아니다.

## 설치

파일은 `AGENTS.md` 하나뿐이다. 사본 하나를 두고 에이전트가 규칙을 읽는 곳마다 링크하라.

```bash
curl -fsSL --create-dirs -o ~/seam-arch/AGENTS.md https://raw.githubusercontent.com/eugeneliukindev/seam-arch/main/AGENTS.md

mkdir -p ~/.claude/rules && ln -s ~/seam-arch/AGENTS.md ~/.claude/rules/seam-arch.md   # Claude Code
ln -s ~/seam-arch/AGENTS.md ~/.codex/AGENTS.md                                       # Codex
ln -s ~/seam-arch/AGENTS.md ~/.gemini/GEMINI.md                                      # Gemini CLI
ln -s ~/seam-arch/AGENTS.md ~/.config/opencode/AGENTS.md                             # opencode
ln -s ~/seam-arch/AGENTS.md ./AGENTS.md          # one project: Cursor, Copilot, Zed and any agent that reads AGENTS.md
```

같은 `curl`을 다시 실행하면 모든 에이전트가 한꺼번에 갱신된다.

## 과제

각 과제는 작은 저장소의 평범한 티켓이다. 에이전트가 보지 못하는 숨은 검사가 설계를 본다. 숫자는 통과한 언어의 수다. ✗와 ✓는 Python 결과로, 다른 언어는 아직 측정하지 않았다.

| 과제 | 에이전트가 받는 요청 | 숨은 검사가 보는 것 | AGENTS.md 없이 | AGENTS.md 있이 |
|---|---|---|:-:|:-:|
| `heavy-decision` | 이력서 요약: 파일을 읽고 등급을 매긴다 | DIP: 파일 리더는 매개변수로 들어온다 | 0/6 | 6/6 |
| `notify-channel` | 사용자는 이메일 대신 SMS를 고를 수 있다 | OCP: 새 채널은 분기가 아니라 새 클래스 | 1/6 | 6/6 |
| `password-login` | 로그인 추가, scrypt로 해시 | DIP: 해싱은 서비스 안이 아니라 계약 뒤에 | 0/6 | 6/6 |
| `combo-checkout` | 만료일이 있는 쿠폰, 국가별 VAT, Stripe로 결제 | 필요한 곳에만 이음새: 시간은 밖에서, VAT는 데이터, Stripe 래퍼 없음 | 1/6 | 2/6 |
| `combo-alerts` | 이메일 대체가 있는 SMS, 두 번째 세션에서 푸시 | SOLID: 채널에 따른 분기 없음, 메서드 하나짜리 계약, 모든 notifier가 이를 지킴 | ✗ | ✓ |
| `coupon-expiry` | 만료된 쿠폰 거절 | DIP: 시계는 밖에서 들어온다 | ✗ | ✓ |
| `humble-cli` | CLI에 --overdue 추가 | Humble Object: CLI는 파싱과 출력만 한다 | ✗ | ✓ |
| `plain-records` | 날씨 예보 API로 우산 조언 | 경계: 원시 페이로드는 가장자리에서 레코드가 된다 | ✗ | ✓ |
| `second-channel` | SMS, 두 번째 세션에서 푸시 | 두 번 수정한 뒤의 OCP | ✗ | ✓ |
| `speculative-abstraction` | Stripe로 결제, "나중에 PayPal도 될지 모름" | 균형추: 클라이언트 하나에 인터페이스 없음 | 6/6 | 6/6 |

## 출처

- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)와 *Clean Architecture*: 의존성 규칙, SOLID, Humble Object, 경계.
- Michael Feathers, *Working Effectively with Legacy Code*: 이음새.
- Miško Hevery, [Guide: Writing Testable Code](https://github.com/mhevery/guide-to-testable-code): 협력자는 요청하고, 직접 가져오지 않는다.
- Robert C. Martin, *Clean Code*: 플래그 인수, 서드파티 API 감싸기.
- [Google style guides](https://google.github.io/styleguide/cppguide.html#Parting_Words): 주변 코드를 따르라.
- Alexis King, [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/): 경계에서 검증하라.

## 라이선스

[MIT](../LICENSE).
