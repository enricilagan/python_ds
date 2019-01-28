import thanksgiving


def main():
    print("This is to explore Thanksgiving in the United States.")
    print()
    thanksgiving.init()

    print("Please choose from the following Region:")
    region = sorted(thanksgiving.region())
    region.remove('')
    for idx, reg in enumerate(region):
        print(f'{idx+1}. {reg}')
    choice = input("Enter region name or number from above: ")
    if choice in region:
        region_choice = choice
    elif choice in [str(x) for x in range(1, len(region)+1)]:
        region_choice = region[int(choice) - 1]
    else:
        raise ValueError
    print()

    print("Enter income range from the following option:")
    income = sorted(thanksgiving.income(region_choice))
    for idx, reg in enumerate(income):
        print(f'{idx+1}. {reg}')
    choice = input("Enter Income Range: ")
    if choice in income:
        income_choice = choice
    elif choice in [str(x) for x in range(1, len(income)+1)]:
        income_choice = income[int(choice) - 1]
    else:
        raise ValueError
    print()

    print(f'You have chosen region {region_choice} with income range of {income_choice}')
    print()

    print('... Choosing a Region and Income Appropriate Menu:')
    main_dish, cooked, cranberry, gravy = thanksgiving.main_dish_selection(region_choice, income_choice)
    print(f'Main dish: {cooked} {main_dish} with {cranberry} Cranberry sauce {"and Gravy" if gravy == "Yes" else ""}')
    print()

    print('... Choosing 3 sides')
    sides = thanksgiving.side_dishes(region_choice, income_choice)
    # print(sides)
    print(f'Side dishes: {sides[0]}, {sides[1]} and {sides[2]}')
    print()

    print('... Choosing which pie')
    pie = thanksgiving.which_pie(region_choice, income_choice)
    print(f'The perfect pie: {pie} Pie')
    print()

    print('... Choosing which dessert')
    desserts = thanksgiving.desserts(region_choice, income_choice)
    print(f'For dessert: {"No Desserts" if desserts == "None" else desserts}')
    print()

    # Collecting Everything
    print(f'The Menu for Thanksgiving for a family earning {income_choice} living in {region_choice}')
    print(f'{cooked} {main_dish} with {cranberry} Cranberry sauce '
          f'{"and Gravy" if gravy == "Yes" else ""} as main dish')
    print(f'{sides[0]}, {sides[1]} and {sides[2]} on the sides')
    print(f'with {pie} Pie for the perfect pie and {desserts} for dessert.')


if __name__ == '__main__':
    main()
