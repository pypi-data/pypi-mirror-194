from typing import Dict, List
from python_on_whales import docker, Image, DockerException
from .config.build_config import ImageBuildConfig


def build_image_dest(tag: str):
    return f"./{tag.replace('/', '_').replace(':', '_')}.tar"


def build_platform_tag(tag: str, version: str, platform: str):
    return f"{tag}:{version}-{platform.replace('/', '-')}"


def build_image(tag: str, version: str, config: ImageBuildConfig) -> List[Image]:
    buildx_builder = docker.buildx.create(
        use=True,
        driver="docker-container",
        driver_options={"network": "host"},
        buildkitd_flags="--allow-insecure-entitlement network.host",  # Allows for network host option for building in Argo
    )

    images = []
    with buildx_builder:
        for platform in config.platforms:
            print(f"Building image {tag}:{version} for platform {platform}")
            image = docker.build(
                config.context_dir,
                build_args=config.build_args,
                tags=build_platform_tag(tag, version, platform),
                cache=config.cache,
                file=config.dockerfile,
                secrets=[
                    f"id={secret.id},src={secret.src}" for secret in config.secrets
                ],
                platforms=[platform],
                progress=config.progress,
                network=config.network,
                output={
                    "type": "docker",
                    "name": build_platform_tag(tag, version, platform),
                },
            )

            images.append(image)

    return images


def publish_image(tag: str, version: str, config: ImageBuildConfig):
    images = []
    latest_images = []

    for platform in config.platforms:
        img_tag = build_platform_tag(tag, version, platform)
        docker.push(img_tag)
        images.append(img_tag)

        latest_tag = build_platform_tag(tag, "latest", platform)
        docker.tag(img_tag, latest_tag)
        docker.push(latest_tag)
        latest_images.append(latest_tag)

    docker.manifest.create(name=f"{tag}:{version}", manifests=images)

    docker.manifest.push(f"{tag}:{version}", purge=True)

    docker.manifest.create(name=f"{tag}:latest", manifests=latest_images)

    docker.manifest.push(f"{tag}:latest", purge=True)


def pull_images(
    tag: str, version, config: ImageBuildConfig, platforms: List[str] = None
) -> Dict[str, Image]:
    images = {}

    if platforms is None:
        platforms = config.platforms

    for platform in platforms:
        try:
            img = docker.pull(build_platform_tag(tag, version, platform))
            images[platform] = img
        except DockerException as e:
            pass

    if len(images) == 0:
        images["none"] = docker.pull(f"{tag}:{version}")

    return images


def deploy_images(
    image_dict: Dict[str, Image],
    target_tag: str,
    version: str,
    config: ImageBuildConfig,
    target_platform: str = None,
):
    images = []

    if "none" in image_dict:
        img = image_dict.get("none")

        if img is not None:
            new_tag = f"{target_tag}:{version}"
            img.tag(new_tag)
            docker.push(new_tag)

            return
    if target_platform is not None:
        img = image_dict.get(target_platform)

        if img is None:
            raise Exception(
                f"Cannot find image for {target_tag}:{version} on target platform {target_platform}"
            )

        new_tag = f"{target_tag}:{version}"
        img.tag(new_tag)
        docker.push(new_tag)
        return

    for platform in config.platforms:
        img = image_dict.get(platform)

        if img is not None:
            new_tag = build_platform_tag(target_tag, version, platform)
            img.tag(new_tag)
            docker.push(new_tag)
            images.append(new_tag)

    docker.manifest.create(name=f"{target_tag}:{version}", manifests=images)

    docker.manifest.push(f"{target_tag}:{version}", purge=True)
