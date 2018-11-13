select distinct player from (
        select winner as player from atpworldtours
        union
        select loser as player from atpworldtours
)tt
where player ilike '%{player}%'
limit 10"
