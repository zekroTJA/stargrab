import config
import github
import repo
import util


def main() -> int:
    cfg = config.parse()
    client = github.Client(cfg.get("github_token"))
    repos = client.get_starred_repositories(cfg.get("user"))

    repos = util.filter_ignore(cfg, repos)
    repos_len = len(repos)

    repo.store_meta(cfg.get("target"), repos)

    print(
        f"Start mirroring {len(repos)} "
        f"repositories to {cfg.get('target')} ...")

    successful, failed = 0, 0
    for i, r in enumerate(repos):
        print(f"[{i}/{repos_len}] Mirroring {r.owner_login}/{r.name} ...")
        try:
            repo.mirror(cfg.get("target"), r, cfg.get("depth"))
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
