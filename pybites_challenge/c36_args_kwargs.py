def get_profile(profile, age, *sports, **awards):
    if type(age) != int or len(sports) > 5:
        raise ValueError
    profile = {'name': profile, 'age': age}
    if sports:
        profile['sports'] = sorted(list(sports))
    if awards:
        profile['awards'] = awards
    return profile


print(get_profile('tim', 36, 'tennis', 'basketball', champ='helped out team in crisis'))