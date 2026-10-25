<p align="center">
  <img src="../assets/hero.png" width="880" alt="seam-arch：6 言語で設計チェック 35 件中 31 件を達成（なしでは 8 件）、動作チェックはすべて合格。">
</p>

<p align="center">
  <em>コードの置き場所は彼が決める。間違った場所には何も置かれない。</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/one%20file-379%20words-111111?style=flat-square" alt="1 ファイル、379 語">
  <img src="https://img.shields.io/badge/built%20on-Clean%20Architecture-111111?style=flat-square" alt="Clean Architecture に基づく">
  <img src="https://img.shields.io/badge/measured-6%20languages-111111?style=flat-square" alt="6 言語で計測">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT ライセンス">
</p>

<p align="center">
  <a href="#例">例</a> &middot;
  <a href="#数値">数値</a> &middot;
  <a href="#インストール">インストール</a> &middot;
  <a href="#タスク">タスク</a> &middot;
  <a href="#出典">出典</a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.ru.md">Русский</a> &middot; <a href="README.es.md">Español</a> &middot; <a href="README.ko.md">한국어</a> &middot; <a href="README.zh-CN.md">简体中文</a> &middot; <strong>日本語</strong></sub>
</p>

---

**seam-arch** は、コーディングエージェントにアーキテクチャを教える 1 つの `AGENTS.md` だ。コードをどこに置き、各部分がどう依存し合うか。軸になる問いは 1 つ：*別のやり方にしたら、プログラムの判断は何か変わるか？* 変わらないなら、それは詳細であり、テストで差し替えられる型を通してのみビジネスロジックに届く。

> [!NOTE]
> Robert C. Martin の *Clean Architecture* に基づく：依存性のルール、SOLID、Humble Object、境界を越えるのはプレーンなデータ。どのルールも、それがなければエージェントが失敗するタスクで存在理由を示している。

## 例

ベンチマークの実際の出力を抜粋したもの。画像はプレビューで、その下の言語を開くと、エージェントがその言語で書いたコードが見られる。

### 1. アラート：1 つのサービスで SOLID

**「ユーザーはメールの代わりに SMS を選べる。電話番号がなければメール。次に：プッシュ。」** Python、3 回の実行：AGENTS.md なしで 0/3、ありで 3/3。

<p align="center">
  <img src="../assets/case-alerts.png" width="880" alt="seam-arch なしでは、サービスがチャネルで分岐する。seam-arch ありでは、Notifier 契約が 1 つ、チャネルごとに独自のフォールバックを持つクラスがあり、エントリポイントで選ばれる。">
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

### 2. チェックアウト：シームは必要な場所にだけ

**「有効期限付きクーポン、国別の VAT、Stripe で課金。PayPal はそのうち。」** Python、3 回の実行：AGENTS.md なしで 0/3、ありで 3/3。最も難しいタスク：他の言語では、エージェントは 5 回中 4 回でまだ Stripe をラップしている。

<p align="center">
  <img src="../assets/case-checkout.png" width="880" alt="seam-arch なしでは、誰も必要としない PaymentGateway ラッパーと、内部で読まれる時計。seam-arch ありでは、時刻は外から渡され、VAT はテーブル、Stripe 自身のクラスがそのまま使われる。">
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

時刻は判断を左右するので、外から渡す。VAT はデータなので、テーブルのまま。Stripe のクラスはすでにフェイクにできるので、ラッパーは付けない。

### 3. パスワード：契約の向こうにある詳細

**「アカウントにはパスワードが必要。scrypt とランダムなソルトでハッシュする。」** AGENTS.md なしで 0/6 言語、ありで 6/6。

<p align="center">
  <img src="../assets/case-password.png" width="880" alt="seam-arch なしでは、サービスが hashlib を import して自分で scrypt を実行する。seam-arch ありでは、PasswordHasher 契約があり、サービスはそれを呼び、エントリポイントが ScryptHasher を選ぶ。">
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

誰がログインできるかを決めるのはサービスだ。バイトをどうハッシュするかは詳細であり、タスクがその方式を名指しし、標準ライブラリにそれがあっても変わらない。

## 数値

同じエージェントを AGENTS.md あり・なしで実行。

| 言語 | 設計タスク | AGENTS.md なし | AGENTS.md あり |
|---|:-:|:-:|:-:|
| Python | 10 | 2/10 | **10/10** |
| TypeScript | 5 | 1/5 | **4/5** |
| Go | 5 | 1/5 | **4/5** |
| Java | 5 | 2/5 | **4/5** |
| C# | 5 | 1/5 | **5/5** |
| Rust | 5 | 1/5 | **4/5** |

どの言語にも同じ 10 タスクがあり、Python 以外ではこれまでに 5 タスクを計測した。`speculative-abstraction` は歯止めで、ルールが過剰設計すると失敗する。動作チェックはどちらでもすべて合格する。seam-arch が変えるのはコードの置き場所であり、動くかどうかではない。

## インストール

ファイルは `AGENTS.md` だけ。コピーを 1 つ置き、エージェントがルールを読む場所すべてにリンクする：

```bash
curl -fsSL --create-dirs -o ~/seam-arch/AGENTS.md https://raw.githubusercontent.com/eugeneliukindev/seam-arch/main/AGENTS.md

mkdir -p ~/.claude/rules && ln -s ~/seam-arch/AGENTS.md ~/.claude/rules/seam-arch.md   # Claude Code
ln -s ~/seam-arch/AGENTS.md ~/.codex/AGENTS.md                                       # Codex
ln -s ~/seam-arch/AGENTS.md ~/.gemini/GEMINI.md                                      # Gemini CLI
ln -s ~/seam-arch/AGENTS.md ~/.config/opencode/AGENTS.md                             # opencode
ln -s ~/seam-arch/AGENTS.md ./AGENTS.md          # one project: Cursor, Copilot, Zed and any agent that reads AGENTS.md
```

同じ `curl` をもう一度実行すれば、すべてのエージェントが一度に更新される。

## タスク

各タスクは小さなリポジトリにある普通のチケットで、エージェントには見えない隠しチェックが設計を確認する。数字は合格した言語の数。✗ と ✓ は Python の結果で、他の言語はまだ計測していない。

| タスク | エージェントへの依頼 | 隠しチェックが見るもの | AGENTS.md なし | AGENTS.md あり |
|---|---|---|:-:|:-:|
| `heavy-decision` | 履歴書を要約：ファイルを読み、評価する | DIP：ファイル読み込みはパラメータとして渡される | 0/6 | 6/6 |
| `notify-channel` | ユーザーはメールの代わりに SMS を選べる | OCP：新しいチャネルは分岐ではなく新しいクラス | 1/6 | 6/6 |
| `password-login` | ログインを追加、scrypt でハッシュ | DIP：ハッシュ処理はサービス内ではなく契約の向こう | 0/6 | 6/6 |
| `combo-checkout` | 有効期限付きクーポン、国別の VAT、Stripe で課金 | シームは必要な場所にだけ：時刻は外から、VAT はデータ、Stripe にラッパーなし | 1/6 | 2/6 |
| `combo-alerts` | メールへのフォールバック付き SMS、続いて 2 回目のセッションでプッシュ | SOLID：チャネルで分岐しない、メソッド 1 つの契約、すべての通知クラスがそれを守る | ✗ | ✓ |
| `coupon-expiry` | 期限切れクーポンを拒否 | DIP：時計は外から来る | ✗ | ✓ |
| `humble-cli` | CLI に --overdue を追加 | Humble Object：CLI はパースと出力だけ | ✗ | ✓ |
| `plain-records` | 天気予報 API から傘のアドバイス | 境界：生のペイロードは端でレコードになる | ✗ | ✓ |
| `second-channel` | SMS、続いて 2 回目のセッションでプッシュ | 2 回の編集を経た OCP | ✗ | ✓ |
| `speculative-abstraction` | Stripe で課金、「PayPal はそのうち」 | 歯止め：クライアント 1 つのためにインターフェースを作らない | 6/6 | 6/6 |

## 出典

- Robert C. Martin、[The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) と *Clean Architecture*：依存性のルール、SOLID、Humble Object、境界。
- Michael Feathers、*Working Effectively with Legacy Code*：シーム。
- Miško Hevery、[Guide: Writing Testable Code](https://github.com/mhevery/guide-to-testable-code)：協調オブジェクトは自分で取りに行かず、渡してもらう。
- Robert C. Martin、*Clean Code*：フラグ引数、サードパーティ API のラップ。
- [Google スタイルガイド](https://google.github.io/styleguide/cppguide.html#Parting_Words)：周囲のコードに従う。
- Alexis King、[Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)：境界で検証する。

## ライセンス

[MIT](../LICENSE)。
