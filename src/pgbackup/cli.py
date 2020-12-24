from argparse import Action, ArgumentParser

known_drivers = ['local', 's3']

class DriverAction(Action):
	def __call__(self, parser, namespace, values, option_string=None):
		driver, destination= values
		if driver.lower() not in known_drivers:
		 parser.error("Unknown driver. Available drivers are 'local' & 's3'")
		namespace.driver = driver.lower()
		namespace.destination = destination
def main():
    import boto3
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 's3':
     client = boto3.client('s3')
     # TODO: create a better name based on the database name and the date
     storage.s3(client, dump.stdout, args.destination, 'example.sql')
    else:
     outfile = open(args.destination, 'wb')
     storage.local(dump.stdout, outfile)

def create_parser():
	parser = ArgumentParser(description="""
	Backup PostgreSQL DBs locally or to AWS S3.
	""")
	parser.add_argument('url', help="URL of database to backup")
	parser.add_argument('--driver',
		help="how & where to store backup",
		nargs=2,
		action=DriverAction,
		required=True)
	return parser
