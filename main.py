import math
import random
import statistics

# Change to your local currency if desired.
currency_symbol = "$"
cost_of_20000_gems = 99.99

def main():

    # Here are some example usages. Feel free to change one to the lands you're
    # still missing, delete the ones you don't want, or increase the number of
    # runs for better accuracy.

    # 1. I want to collect every land in the set (except Rainbow, which can be crafted).
    desired_lands = [m for m in mythics if m != "Rainbow"] + rares + commons
    simulate(desired_lands, 1000)

    # 2. I want to collect all the mythic lands (except Rainbow, which can be crafted).
    desired_lands = [m for m in mythics if m != "Rainbow"]
    simulate(desired_lands, 1000)

    # 3. I want to collect the five planeswalker lands.
    desired_lands = ["Basri", "Teferi", "Liliana", "Chandra", "Garruk"]
    simulate(desired_lands, 1000)

    # 4. I just want to collect a phrexian swamp (mythic rarity).
    desired_lands = ["Phyrexian"]
    simulate(desired_lands, 1000)

    # 5. I just want to collect a goblin mountain to ruin historic (common rarity).
    desired_lands = ["Goblins"]
    simulate(desired_lands, 1000)



# List of themes and rarities, don't change these.
mythics = ["Basri", "Unicorns", "Teferi", "Mill", "Liliana", "Phyrexian", "Chandra", "Seismic", "Garruk", "Walls", "Rainbow"]
rares = ["Angels", "Dogs", "Enchanted", "Pirates", "Spirits", "Under the Sea", "Discarding", "Rogues", "Witchcraft", "Dragons", "Lightning", "Minotaurs", "Cats", "Elves", "Lands"]
commons = ["Doctor", "Feathered Friends", "Heavily Armored", "Legion", "Above the Clouds", "Archaeology", "Well-Read", "Wizards", "Minions", "Reanimated", "Spooky", "Vampires", "Devilish", "Goblins", "Smashing", "Spellcasting", "Dinosaurs", "Plus One", "Predatory", "Tree-Hugging"]

# Random packs will be picked from this list. Duplicates used for weighting.
packs = mythics.copy()
for rare in rares:
    packs.extend([rare, rare])
for common in commons:
    packs.extend([common, common, common, common])

# Each run of the simulation will start with an empty collection and repeatedly
# draw three packs, picking the best one to progress the collection. At the end
# it prints out some statistics.
def simulate(desired_themes, number_of_runs):
    results = []
    while len(results) < number_of_runs:
        collection = {}
        count = 0.0

        # We'll add a key to our collection for each theme as we choose it and
        # stop the current run when our collection is finished.
        while len(collection.keys()) < len(desired_themes):

            # Each set of three packs counts as half an entry since you choose twice.
            count += 0.5

            # Each set will have three unique packs. However, there's no
            # duplicate protection between the first set of three and the next
            # set of three, so we can treat them independently.
            first = random.choice(packs)
            second = random.choice([p for p in packs if p != first])
            third = random.choice([p for p in packs if p != first and p != second])

            # Pretty simple strategy to complete the collection. First prioritize
            # new mythics, then new rares, then new commons. When there's a tie,
            # just pick the leftmost pack.
            if first in mythics and first in desired_themes and first not in collection:
                collection[first] = True
            elif second in mythics and second in desired_themes and second not in collection:
                collection[second] = True
            elif third in mythics and third in desired_themes and third not in collection:
                collection[third] = True
            elif first in rares and first in desired_themes and first not in collection:
                collection[first] = True
            elif second in rares and second in desired_themes and second not in collection:
                collection[second] = True
            elif third in rares and third in desired_themes and third not in collection:
                collection[third] = True
            elif first not in collection and first in desired_themes:
                collection[first] = True
            elif second not in collection and second in desired_themes:
                collection[second] = True
            elif third not in collection and third in desired_themes:
                collection[third] = True

        # Even if you only needed the first pack, you pay for the whole entry.
        results.append(math.ceil(count))

        # Delete this if you don't want it to periodically print the progress.
        if (0 == len(results) % 1000):
            print("{} of {} runs completed ({:.1f}%)".format(len(results), number_of_runs,
                len(results) * 100.0 / number_of_runs))

    print_results(desired_themes, results)

def currency_from_entries(entries):
    jumpstart_gems = 400
    return "{}{:.2f}".format(currency_symbol,
            ((entries * jumpstart_gems) / 20_000) * cost_of_20000_gems)

def print_results(desired_themes, results):
    mean = statistics.mean(results)
    std_dev = statistics.stdev(results)
    min_entries = math.ceil(len(desired_themes) / 2.0)
    print("Desired themes: {}".format(", ".join(desired_themes)))
    print("Average number of entries to complete:{:>10.2f}".format(mean))
    print("Average cost to complete:{:>23}".format(currency_from_entries(mean)))
    print("Minimum cost to complete:{:>23}".format(currency_from_entries(min_entries)))
    print("68% of players will pay between{:>17}    and{:>15}".format(
        max(currency_from_entries(min_entries),
            currency_from_entries(mean - std_dev)),
        currency_from_entries(mean + std_dev)))
    print("95% of players will pay between{:>17}    and{:>15}".format(
        max(currency_from_entries(min_entries),
            currency_from_entries(mean - 2 * std_dev)),
        currency_from_entries(mean + 2 * std_dev)))
    print("16% of players will pay at least{:>16}".format(
        currency_from_entries(mean + std_dev)))
    print("16% of players will pay{:>25}    or less".format(
        max(currency_from_entries(min_entries),
            currency_from_entries(mean - std_dev))))
    print("2% of players will pay at least{:>17}".format(
        currency_from_entries(mean + 2 * std_dev)))
    print("2% of players will pay{:>26}    or less\n".format(
        max(currency_from_entries(min_entries),
            currency_from_entries(mean - 2 * std_dev))))

if __name__ == "__main__":
    main()
