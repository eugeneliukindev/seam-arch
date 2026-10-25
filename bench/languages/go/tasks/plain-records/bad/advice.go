// Package weather tells people what to wear and carry, from the forecast.
package weather

import (
	"context"
	"fmt"
)

// rainThreshold is the chance of rain above which an umbrella is worth carrying.
const rainThreshold = 0.5

// ShouldTakeUmbrella reports whether rain is more likely than not in city today.
func ShouldTakeUmbrella(ctx context.Context, city string, api *ForecastAPI) (bool, error) {
	payload, err := api.Fetch(ctx, city)
	if err != nil {
		return false, err
	}
	days, _ := payload["daily"].([]any)
	if len(days) == 0 {
		return false, fmt.Errorf("no forecast for %s", city)
	}
	today, _ := days[0].(map[string]any)
	chance, _ := today["pop"].(float64)
	return chance > rainThreshold, nil
}
