require "json"
require "open-uri"

class FmController < ApplicationController
  def read
    #읽어오기
    file = File.new("/save_test.json", "r+")
    data = JSON.parse(file.read)
    file.close
    
    fd.puts to_save.to_json
    
    redirect_back fallback_location: "load"
  end
  def save
    #쓰기
    
    if !File.exist? ("./save.json") || File.zero?("./save.json")
      file = File.new("./save.json", "w+")
      to_save = {}
      fd = {}
      fd["game"] = {}
      fd["player"] = {}
      fd["view"] = {}
      fd["selected"] = {}
      to_save["0"] = fd
      to_save["1"] = fd
      to_save["2"] = fd
      file.puts to_save.json
      file.close
    end

    file = File.new("./save.json", "r+")
    to_parse = JSON.parse(file.read)
    file.close
    file = File.new("./save.json", "w+")
    to_save = to_parse["#{$view["fd"]}"]
    to_save["game"] = $game
    to_save["player"] = $player
    to_save["view"] = $view
    to_save["selected"] = $selected
    to_parse["#{$view['fd']}"] = to_save
    file.puts to_parse.to_json
    file.close

    redirect_back fallback_location: "load"
  end
end
