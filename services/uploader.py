
class Uploader:

    @staticmethod
    def upload_video_movies(instance, filename):
        return f"videos/{instance.movie.slug}/{filename}"

    @staticmethod
    def upload_image_movies(instance, filename):
        return f"images/{instance.movie.slug}/{filename}"


    @staticmethod
    def upload_video_episode(instance, filename):
        return f"videos/{instance.episode.slug}/{filename}"

    @staticmethod
    def upload_image_serie(instance, filename):
        return f"images/{instance.serie.slug}/{filename}"

 
