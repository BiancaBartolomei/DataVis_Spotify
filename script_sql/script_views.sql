create or replace view spotify_db.top_musicas_populares as
  select t.track_name, a.artist_name, p.track_popularity,
  p.data_popularidade, a.artist_genre
  from spotify_db.track as t
  inner join spotify_db.track_artist using (track_id)
  inner join spotify_db.artist as a using(artist_id)
  inner join spotify_db.track_popularity as p using (track_id)
  order by data_popularidade;

# ----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.features_track as
  select track_name, track_liveness, track_speechness, track_valence, track_energy, track_acousticness, track_instrumentalness, track_dancebility
  from spotify_db.track;
# ----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.musicas_por_genero
as select count(a.artist_id) as quant, a.artist_genre
from spotify_db.artist a
where a.artist_genre is not null
group by a.artist_genre order by quant desc;

# ----------------------------------------------------------------------------------------------------------------------
create or replace view spotify_db.features_artist as
  select a.artist_name, avg(track_liveness) as track_liveness, avg(track_speechness) as track_speechness,
        avg(track_valence) as track_valence, avg(track_energy) as track_energy, avg(track_acousticness) as track_acousticness, avg(track_instrumentalness) as track_instrumentalness,
         avg(track_dancebility) as track_dancebility
  from spotify_db.track t join spotify_db.track_artist ta on t.track_id = ta.track_id
        join  spotify_db.artist a on ta.artist_id = a.artist_id
  group by a.artist_name;

# ----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.features_playlist as
  select a.playlist_name, avg(track_liveness) as track_liveness, avg(track_speechness) as track_speechness,
        avg(track_valence) as track_valence, avg(track_energy) as track_energy, avg(track_acousticness) as track_acousticness, avg(track_instrumentalness) as track_instrumentalness,
         avg(track_dancebility) as track_dancebility
  from spotify_db.track t join spotify_db.track_playlist ta on t.track_id = ta.track_id
        join  spotify_db.playlist a on ta.playlist_id = a.playlist_id
  group by a.playlist_name;

#-----------------------------------------------------------------------------------------------------------------------

create or replace view spotify_db.explicit_genre
as  select count(t.track_id) as quant, a.artist_genre
from spotify_db.track t join spotify_db.track_artist ta on t.track_id = ta.track_id
join spotify_db.artist a on ta.artist_id = a.artist_id
where track_explicit = 't' and a.artist_genre is not null
group by a.artist_genre order by quant desc;


create or replace view spotify_db.duration_track
as select track_id, track_duration from spotify_db.track;

# ----------------------------------------------------------------------------------------------------------------------
create or replace function spotify_db.top10_tracks(data date) returns table (Track varchar, Popularidade smallint) as $$
begin
  return query select t.track_name, tp.track_popularity
from spotify_db.track t join spotify_db.track_popularity tp on t.track_id = tp.track_id
where tp.data_popularidade = data
order by tp.track_popularity desc
limit 10;
end;
$$ language plpgsql;

# ----------------------------------------------------------------------------------------------------------------------
create or replace function spotify_db.top10_artist(data date) returns table (Artist varchar, Popularidade smallint) as $$
begin
  return query select a.artist_name, ap.artist_popularity
from spotify_db.artist a join spotify_db.artist_popularity ap on a.artist_id = ap.artist_id
where ap.data_popularidade = data
order by ap.artist_popularity desc
limit 10;
end;
$$ language plpgsql;