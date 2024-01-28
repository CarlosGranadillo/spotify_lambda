import spotipy

spotify = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())
print(spotify)

def super_add(num1, num2):
    my_add = num1 + num2

    print('Inside a function!')
    return my_add

print('successfully authenticated!')

print('Testing breakpoints')

if __name__ == '__main__':
    first_num = 10
    print(first_num)
    second_num = 40
    print(second_num)

    my_result = super_add(first_num, second_num)

    print(my_result)

print('Done!!!')