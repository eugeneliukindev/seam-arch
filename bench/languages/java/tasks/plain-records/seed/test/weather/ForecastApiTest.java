package weather;

final class ForecastApiTest {
    public static void main(String[] args) {
        try {
            new ForecastApi().fetch("Oslo");
            throw new AssertionError("fetch needs the provider");
        } catch (UnsupportedOperationException expected) {
            System.out.println("ForecastApiTest: ok");
        }
    }
}
