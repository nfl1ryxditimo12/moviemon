require 'uri'
require 'json'
require 'net/http'
require 'openssl'

movie_list = File.open("movie_info.json", "a+")
File.readlines("movie_id.txt").each do |id|
    url = URI("https://movie-database-imdb-alternative.p.rapidapi.com/?i=" + id + "&r=json&plot=short")

    http = Net::HTTP.new(url.host, url.port)
    http.use_ssl = true
    http.verify_mode = OpenSSL::SSL::VERIFY_NONE

    request = Net::HTTP::Get.new(url)
    request["x-rapidapi-key"] = '7b03911613msh88f7bd748bc5a51p186a23jsncf34f0be2abd'
    request["x-rapidapi-host"] = 'movie-database-imdb-alternative.p.rapidapi.com'

    response = http.request(request)
    movie_hash = JSON.parse(response.read_body)

    json_hash = {}

    movie_hash.select do |k,v|
        if k == "Title" || k == "Genre" || k == "Year" || k == "Director" || k == "Writer" || k == "Plot" || k == "Poster"
            json_hash[k] = v
        elsif k == "Ratings"
            json_hash[k] = v[0].values[1].split("/")[0]
    end
end
    movie_list << json_hash.to_json << "\n"
end