import teamGen
import asyncio
from poke_env.player import SimpleHeuristicsPlayer
from poke_env import ShowdownServerConfiguration, PlayerConfiguration


db = teamGen.get_meta_json('gen8ou-0.json', year='2022-02/')
top = teamGen.filterbest(db,competition_level = 0.005)

f = open("temp_team.txt", "w")
f.write(teamGen.makeTeam(top))
f.close()

f = open("temp_team.txt", "r")
team_1 = f.read()
f.close()

player = SimpleHeuristicsPlayer(
        player_configuration=PlayerConfiguration("thighss", "showdown"),
        battle_format="gen8ou",
        team=team_1,
        server_configuration=ShowdownServerConfiguration,
)

# user yakouhyakki wants to see how good it becomes
async def main():   

    # Sending challenges to 'your_username'
    # await player.send_challenges("metalskin", n_challenges=1)

    # Accepting one challenge from any user
    # await player.accept_challenges(None, 1)

    # Accepting three challenges from 'your_username'
    # await player.accept_challenges('your_username', 3)

    # Playing 5 games on the ladder
    await player.ladder(5)

    # Print the rating of the player and its opponent after each battle
    for battle in player.battles.values():
        print(battle.rating, battle.opponent_rating)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
