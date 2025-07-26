async def OutputMainMenu(message):
    from Structures.MainMenu import OutputMainMenu
    await OutputMainMenu(message)


async def OutputClaimToPlayerMenu(message):
    from Structures.ClaimToPlayerMenu import OutputClaimToPlayer
    await OutputClaimToPlayer(message)


async def OutputInputFormMenu(message):
    from Structures.InputClaimToPlayer.InputFormMenu import OutputInputFormMenu
    await OutputInputFormMenu(message)


async def OutputBox1Menu(message):
    from Structures.InputClaimToPlayer.Box1Menu import OutputBox1Menu
    await OutputBox1Menu(message)


async def OutputBox2Menu(message):
    from Structures.InputClaimToPlayer.Box2Menu import OutputBox2Menu
    await OutputBox2Menu(message)


async def OutputBox3Menu(message):
    from Structures.InputClaimToPlayer.Box3Menu import OutputBox3Menu
    await OutputBox3Menu(message)


async def OutputBox4Menu(message):
    from Structures.InputClaimToPlayer.Box4Menu import OutputBox4Menu
    await OutputBox4Menu(message)


async def OutputBox5Menu(message):
    from Structures.InputClaimToPlayer.Box5Menu import OutputBox5Menu
    await OutputBox5Menu(message)


async def OutputBox6Menu(message):
    from Structures.InputClaimToPlayer.Box6Menu import OutputBox6Menu
    await OutputBox6Menu(message)
