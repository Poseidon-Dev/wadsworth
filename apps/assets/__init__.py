from apps.assets.models import AssetTable, CategoryTable, StatusTable
from apps.assets.commands import AssetCommands

def setup(bot):
    CategoryTable().run()
    StatusTable().run()
    AssetTable().run()
    bot.add_cog(AssetCommands(bot))

    # Inserting dummy data
    values = "1, 12799, 'email', 1, 'Apple', 'iPhone6', 'HDUSYRE762', 'IMEI', 1, '2018-01-01', '', '' , '0'"
    AssetTable().insert_single_record(values)