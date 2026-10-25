// Package weather tells people what to wear and carry, from the forecast.
package weather

import "context"

// rainThreshold is the chance of rain above which an umbrella is worth carrying.
const rainThreshold = 0.5

// ShouldTakeUmbrella reports whether rain is more likely than not in city today.
func ShouldTakeUmbrella(ctx context.Context, city string, api *ForecastAPI) (bool, error) {
	forecast, err := api.Today(ctx, city)
	if err != nil {
		return false, err
	}
	return forecast.RainChance > rainThreshold, nil
}
