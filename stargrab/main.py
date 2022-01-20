import config
import github
import repo


def main() -> int:
    cfg = config.parse()
    client = github.Client(cfg.get("github_token"))
    repos = client.get_starred_repositories(cfg.get("user"))
    print(
        f"Start mirroring {len(repos)} "
        f"repositories to {cfg.get('target')} ...")
    successful, failed = 0, 0
    for r in repos:
        print(f"Mirroring {r.owner_login}/{r.name} ...")
        try:
            repo.mirror(cfg.get('target'), r)
            successful += 1
        except Exception as e:
            print(f"Error: {e}")
            failed += 1
    print(
        "Finished!\n"
        f"Successfully mirrored: {successful}\n"
        f"Failed mirrors:        {failed}")


if __name__ == "__main__":
    exit(main())
