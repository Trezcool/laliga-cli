from operator import itemgetter
from unittest import TestCase

from click.testing import CliRunner
from laliga import cli, Table


class LaLigaTests(TestCase):
    def test_cli__smoke(self):
        """ smoke test to ensure the command runs """
        result = CliRunner().invoke(cli, input='1')
        assert result.exit_code == 0
        assert not result.exception
        assert 'Please enter a fixture result' in result.output
        # NOTE: limitation with `click` library, can't fully test the command when it has lots of prompts.. :(

    def test_table_ranking(self):
        results = [
            'Real Madrid 1, Atletico Madrid 0',
            'Barcelona 1, Villareal 0',
            'Atletic Club 1, Villareal 1',
            'Barcelona 3, Real Madrid 1',
            'Real Madrid 4, Real Betis 0',
            'Atletico Madrid 1, Valencia 1',
            'Barcelona 1, Real Madrid 1',
            'Atletico Madrid 1, Celta Vigo 0',
        ]
        table = Table()
        for result in results:
            table.update(result)

        # teams with same points should be ordered alphabetically
        # Barcelona and Real Madrid should be first
        pos = itemgetter(0)
        team_res = itemgetter(1)
        final_ranking = table.get_final_ranking()
        assert set(table.first_place) == {'Barcelona', 'Real Madrid'}
        assert [team_res(r) for r in final_ranking if pos(r) == 1] == [('Barcelona', 7), ('Real Madrid', 7)]

        # Real Betis and Celta Vigo should be last
        last_pos = pos(final_ranking[table.size - 1])
        assert set(table.last_place) == {'Celta Vigo', 'Real Betis'}
        assert [team_res(r) for r in final_ranking if pos(r) == last_pos] == [('Celta Vigo', 0), ('Real Betis', 0)]
