from quizapi.db import player_table, quiz_table

print("Type of player_table.c.id:", type(player_table.c.id))
print("Type of quiz_table.c.player_id:", type(quiz_table.c.player_id))