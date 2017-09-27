import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
TEXT_INPUT = '1'
FILE_INPUT = '2'


class Table:
    """
    A Soccer league table.
    """
    WIN = 3
    DRAW = 1
    LOSS = 0

    def __init__(self) -> None:
        self.ranking = {}
        self.first_place = []
        self.last_place = []

    def update(self, result: str) -> None:
        """
        Updates the table's ranking with the result of the given fixture.
        """
        team1_score, team2_score = result.strip().split(sep=',')
        team1, score1 = team1_score.strip().rsplit(sep=' ', maxsplit=1)
        team2, score2 = team2_score.strip().rsplit(sep=' ', maxsplit=1)
        score1 = int(score1)
        score2 = int(score2)
        if score1 > score2:
            self.ranking[team1] = self.ranking.get(team1, 0) + self.WIN
            self.ranking[team2] = self.ranking.get(team2, 0) + self.LOSS
        elif score1 < score2:
            self.ranking[team1] = self.ranking.get(team1, 0) + self.LOSS
            self.ranking[team2] = self.ranking.get(team2, 0) + self.WIN
        else:
            self.ranking[team1] = self.ranking.get(team1, 0) + self.DRAW
            self.ranking[team2] = self.ranking.get(team2, 0) + self.DRAW

    def get_final_ranking(self) -> list:
        """
        Returns the final ranking ordered by points (alphabetically for teams with same points).
        """
        ranking = self.ranking.items()
        # add positions to ranking (teams with same points should have same position)
        points = sorted({r[1] for r in ranking}, reverse=True)
        final_ranking = []
        pos = 1
        for point in points:
            # group teams by points and order them alphabetically
            teams = [(pos, r) for r in ranking if r[1] == point]
            alpha_sorted = sorted(teams, key=lambda x: x[1][0])
            final_ranking.extend(alpha_sorted)
            # set first and last place
            teams_names = [t[1][0] for t in teams]
            if pos == 1:
                self.first_place = teams_names
            else:
                self.last_place = teams_names
            pos += len(teams)  # increment position
        return final_ranking

    @property
    def size(self) -> int:
        """ Returns the total number of teams """
        return len(self.ranking)


@click.command(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    This command calculates the ranking table for a soccer league.
    The fixture result format is: `Barcelona 3, Real Madrid 1`.
    """
    click.secho('Please chose one of the input options below:', bold=True)
    click.echo('\t1) Enter results from the command-line')
    click.echo('\t2) Specify a file containing results')
    input_type = click.prompt('Please select an option', type=click.Choice((TEXT_INPUT, FILE_INPUT)))
    table = Table()
    if input_type == TEXT_INPUT:
        help_msg = '\nEnter fixture results one at a time. When done, just press `Enter` without entering anything.'
        click.secho(help_msg, bold=True)
        while True:
            result = click.prompt('Please enter a fixture result', default='')
            if not result:
                break
            table.update(result)
    else:
        filepath = click.prompt('\nPlease enter the file path', type=click.Path(exists=True))
        with open(filepath) as file:
            for result in file.readlines():
                table.update(result)
    # print ranking
    click.secho('|--------|---------------------------|--------|')
    click.secho('| #\t | {:25} | POINTS |'.format('TEAM'), bold=True)
    click.secho('|--------|---------------------------|--------|')
    for pos, (team, points) in table.get_final_ranking():
        text = '| {pos}\t | {team:25} | {points:^6} |'.format(pos=pos, team=team, points=points)
        fg = team in table.first_place and 'green' or team in table.last_place and 'red' or None
        click.secho(text, fg=fg)
    click.secho('|--------|---------------------------|--------|')
