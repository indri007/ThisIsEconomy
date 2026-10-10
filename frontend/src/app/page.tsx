"use client";

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import CytoscapeComponent from 'react-cytoscapejs';
import { 
  AppBar, 
  Box, 
  CssBaseline, 
  Drawer, 
  IconButton, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText, 
  Toolbar, 
  Typography,
  Card,
  Grid,
  CircularProgress,
  TextField,
  MenuItem,
  Select,
  Chip,
  Divider
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HubIcon from '@mui/icons-material/Hub';
import BubbleChartIcon from '@mui/icons-material/BubbleChart';
import GroupWorkIcon from '@mui/icons-material/GroupWork';
import TagIcon from '@mui/icons-material/Tag';
import EmojiEmotionsIcon from '@mui/icons-material/EmojiEmotions';
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Legend } from 'recharts';

const drawerWidth = 260;
const exploreDrawerWidth = 350;
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#a4de6c', '#f44336'];

export default function DashboardLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('ABSA');
  
  // Data States
  const [snaSummary, setSnaSummary] = useState<any>(null);
  const [elements, setElements] = useState([]);
  const [communities, setCommunities] = useState<number[]>([]);
  const [emotionData, setEmotionData] = useState([]);
  const [sarcasmData, setSarcasmData] = useState<any>(null);
  const [communityData, setCommunityData] = useState<any>(null);
  const [absaData, setAbsaData] = useState<any>(null);
  
  // Hashtag & Emoji States
  const [hashtagSummary, setHashtagSummary] = useState<any>(null);
  const [hashtagElements, setHashtagElements] = useState([]);
  const [emojiSummary, setEmojiSummary] = useState<any>(null);
  const [emojiElements, setEmojiElements] = useState([]);

  // Exploration Panel States
  const [exploreOpen, setExploreOpen] = useState(false);
  const [exploreLoading, setExploreLoading] = useState(false);
  const [exploreData, setExploreData] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  // Network States
  const [search, setSearch] = useState('');
  const [communityFilter, setCommunityFilter] = useState('All');
  const cyRef = useRef<any>(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      axios.get(`${API_URL}/api/sna/summary`),
      axios.get(`${API_URL}/api/sna/network`),
      axios.get(`${API_URL}/api/emotion-distribution`),
      axios.get(`${API_URL}/api/sarcasm/summary`),
      axios.get(`${API_URL}/api/sna/communities`),
      axios.get(`${API_URL}/api/hashtag/summary`),
      axios.get(`${API_URL}/api/hashtag/network`),
      axios.get(`${API_URL}/api/emoji/summary`),
      axios.get(`${API_URL}/api/emoji/network`),
      axios.get(`${API_URL}/api/absa/summary`)
    ]).then(([summaryRes, networkRes, emotionRes, sarcasmRes, communityRes, hashSumRes, hashNetRes, emojiSumRes, emojiNetRes, absaRes]) => {
      setSnaSummary(summaryRes.data);
      
      const elems = networkRes.data.elements || [];
      setElements(elems);
      const uniqueComms = new Set<number>();
      elems.forEach((el: any) => {
        if (el.data.community !== undefined) uniqueComms.add(el.data.community);
      });
      setCommunities(Array.from(uniqueComms).sort((a,b) => a - b));

      setEmotionData(emotionRes.data);
      setSarcasmData(sarcasmRes.data);
      setCommunityData(communityRes.data);
      
      setHashtagSummary(hashSumRes.data);
      setHashtagElements(hashNetRes.data.elements || []);
      setEmojiSummary(emojiSumRes.data);
      setEmojiElements(emojiNetRes.data.elements || []);
      
      setAbsaData(absaRes.data.summary);
      
      setLoading(false);
    }).catch(error => {
      console.error("Error fetching data:", error);
      setLoading(false);
    });
  }, []);

  const handleNodeClick = (type: 'hashtag' | 'emoji', keyword: string) => {
    setExploreOpen(true);
    setExploreLoading(true);
    // Remove # for URL parameter if hashtag
    const param = type === 'hashtag' ? keyword.replace('#', '') : keyword;
    
    axios.get(`${API_URL}/api/explore/${type}/${encodeURIComponent(param)}`)
      .then(res => {
        setExploreData(res.data);
        setExploreLoading(false);
      })
      .catch(err => {
        console.error(err);
        setExploreLoading(false);
      });
  };

  useEffect(() => {
    if (activeTab === 'Network Analysis' && cyRef.current) {
      const cy = cyRef.current;
      cy.batch(() => {
        cy.elements().removeClass('hidden highlighted');
        if (communityFilter !== 'All') {
          cy.nodes().forEach((node: any) => {
            if (node.data('community').toString() !== communityFilter) {
              node.addClass('hidden');
              node.connectedEdges().addClass('hidden');
            }
          });
        }
        if (search.trim() !== '') {
          const lowerSearch = search.toLowerCase();
          cy.nodes().forEach((node: any) => {
            if (node.data('label').toLowerCase().includes(lowerSearch)) {
              node.addClass('highlighted');
            }
          });
        }
      });
    }
  }, [search, communityFilter, activeTab]);

  const stylesheet = [
    { selector: 'node', style: { 'label': 'data(label)', 'width': 'mapData(degree, 0, 0.1, 20, 60)', 'height': 'mapData(degree, 0, 0.1, 20, 60)', 'background-color': (ele: any) => colors[ele.data('community') % colors.length], 'font-size': '10px', 'text-valign': 'bottom' as const, 'text-halign': 'center' as const, 'color': '#333', 'text-outline-width': 2, 'text-outline-color': '#fff' } },
    { selector: 'edge', style: { 'width': 1, 'line-color': '#ccc', 'target-arrow-color': '#ccc', 'target-arrow-shape': 'triangle' as const, 'curve-style': 'bezier' as const, 'opacity': 0.5 } },
    { selector: '.hidden', style: { 'display': 'none' } },
    { selector: '.highlighted', style: { 'border-width': 4, 'border-color': '#000', 'width': 50, 'height': 50, 'font-size': '14px', 'z-index': 100 } }
  ];

  const hashStylesheet = [
    { selector: 'node', style: { 'label': 'data(label)', 'width': 'mapData(frequency, 1, 100, 20, 80)', 'height': 'mapData(frequency, 1, 100, 20, 80)', 'background-color': '#1976d2', 'font-size': '12px', 'text-valign': 'center' as const, 'text-halign': 'center' as const, 'color': '#fff' } },
    { selector: 'edge', style: { 'width': 'mapData(weight, 1, 20, 1, 10)', 'line-color': '#90caf9', 'curve-style': 'bezier' as const, 'opacity': 0.6 } }
  ];

  const emojiStylesheet = [
    { selector: 'node', style: { 'label': 'data(label)', 'width': 'mapData(frequency, 1, 100, 30, 90)', 'height': 'mapData(frequency, 1, 100, 30, 90)', 'background-color': '#ffb74d', 'font-size': '30px', 'text-valign': 'center' as const, 'text-halign': 'center' as const, 'background-opacity': 0 } },
    { selector: 'edge', style: { 'width': 'mapData(weight, 1, 20, 1, 10)', 'line-color': '#ffe0b2', 'curve-style': 'bezier' as const, 'opacity': 0.6 } }
  ];

  const menuItems = [
    { text: 'Network Analysis', icon: <HubIcon /> },
    { text: 'Community Analysis', icon: <GroupWorkIcon /> },
    { text: 'Emotion & Sarcasm', icon: <BubbleChartIcon /> },
    { text: 'Hashtag Network', icon: <TagIcon /> },
    { text: 'Emoji Network', icon: <EmojiEmotionsIcon /> },
    { text: 'ABSA', icon: <QueryStatsIcon /> },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ width: { sm: `calc(100% - ${drawerWidth}px)` }, ml: { sm: `${drawerWidth}px` }, backgroundColor: '#fff', color: '#000', boxShadow: 1 }}>
        <Toolbar>
          <IconButton edge="start" onClick={() => setMobileOpen(!mobileOpen)} sx={{ mr: 2, display: { sm: 'none' } }}><MenuIcon /></IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 500 }}>{activeTab}</Typography>
        </Toolbar>
      </AppBar>
      
      {/* Navigation Drawer */}
      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer variant="permanent" sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { width: drawerWidth, borderRight: '1px solid #e0e0e0' } }} open>
          <div>
            <Toolbar><Typography variant="h6" sx={{ fontWeight: 'bold', color: '#1976d2' }}>Tesis MBG</Typography></Toolbar>
            <List>
              {menuItems.map((item) => (
                <ListItem key={item.text} disablePadding>
                  <ListItemButton selected={activeTab === item.text} onClick={() => setActiveTab(item.text)}>
                    <ListItemIcon sx={{ color: activeTab === item.text ? '#1976d2' : 'inherit' }}>{item.icon}</ListItemIcon>
                    <ListItemText primary={item.text} sx={{ color: activeTab === item.text ? '#1976d2' : 'inherit' }} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </div>
        </Drawer>
      </Box>

      {/* Explore Panel Drawer (Right side) */}
      <Drawer
        anchor="right"
        open={exploreOpen}
        onClose={() => setExploreOpen(false)}
        sx={{
          '& .MuiDrawer-paper': { width: exploreDrawerWidth, p: 3, boxSizing: 'border-box' },
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h5" fontWeight="bold">
            <SearchIcon sx={{ verticalAlign: 'middle', mr: 1, color: '#1976d2' }}/>
            {exploreData?.keyword || 'Eksplorasi'}
          </Typography>
          <IconButton onClick={() => setExploreOpen(false)}><CloseIcon /></IconButton>
        </Box>

        {exploreLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}><CircularProgress /></Box>
        ) : exploreData ? (
          <Box>
            <Typography variant="subtitle1" color="text.secondary" gutterBottom>
              Ditemukan dalam <b>{exploreData.total_tweets}</b> Tweets
            </Typography>
            <Divider sx={{ my: 2 }} />

            {/* Emotion */}
            <Typography variant="h6" fontSize="1rem" fontWeight="bold" gutterBottom>Emotion</Typography>
            <Box sx={{ height: 180, width: '100%', mb: 3 }}>
              <ResponsiveContainer>
                <BarChart data={exploreData.emotions} layout="vertical" margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                  <XAxis type="number" hide />
                  <YAxis dataKey="label" type="category" width={70} tick={{ fontSize: 12 }} />
                  <Tooltip cursor={{fill: '#f5f5f5'}} />
                  <Bar dataKey="count" fill="#8884d8" radius={[0, 4, 4, 0]}>
                     {exploreData.emotions.map((entry: any, index: number) => <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </Box>

            {/* Sarcasm */}
            <Typography variant="h6" fontSize="1rem" fontWeight="bold" gutterBottom>Sarcasm</Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
              <Chip label={`Sarkasme: ${exploreData.sarcasm.sarkasme}`} color="error" variant="outlined" sx={{ flex: 1 }} />
              <Chip label={`Non-Sarkasme: ${exploreData.sarcasm.non_sarkasme}`} color="success" variant="outlined" sx={{ flex: 1 }} />
            </Box>

            {/* Top Communities */}
            <Typography variant="h6" fontSize="1rem" fontWeight="bold" gutterBottom>Top Communities</Typography>
            <List dense sx={{ mb: 2 }}>
              {exploreData.communities.map((c: any, i: number) => (
                <ListItem key={i} disableGutters>
                  <ListItemIcon sx={{ minWidth: 30 }}><GroupWorkIcon fontSize="small" color="primary"/></ListItemIcon>
                  <ListItemText primary={`Komunitas #${c.community}`} secondary={`${c.count} tweets`} />
                </ListItem>
              ))}
            </List>

            {/* Top Actors */}
            <Typography variant="h6" fontSize="1rem" fontWeight="bold" gutterBottom>Top Actors</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {exploreData.top_actors.map((a: any, i: number) => (
                <Chip key={i} size="small" label={`${a.actor} (${a.count})`} />
              ))}
            </Box>
            
          </Box>
        ) : (
          <Typography color="error">Gagal memuat data.</Typography>
        )}
      </Drawer>
      
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` }, backgroundColor: '#f5f7fa', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Toolbar />
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 10 }}><CircularProgress /></Box>
        ) : (
          <>
            {activeTab === 'Network Analysis' && (
              <>
                <Card sx={{ mb: 3, p: 2 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={6}>
                      <TextField fullWidth label="Search actor..." variant="outlined" size="small" value={search} onChange={(e) => setSearch(e.target.value)} />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Select fullWidth size="small" value={communityFilter} onChange={(e) => setCommunityFilter(e.target.value)}>
                        <MenuItem value="All">All Communities</MenuItem>
                        {communities.map(c => <MenuItem key={c} value={c.toString()}>Community {c}</MenuItem>)}
                      </Select>
                    </Grid>
                  </Grid>
                </Card>
                <Card sx={{ flexGrow: 1, minHeight: '600px', mb: 3, position: 'relative' }}>
                  <CytoscapeComponent elements={elements} style={{ width: '100%', height: '600px' }} stylesheet={stylesheet} layout={{ name: 'cose', padding: 50 }} cy={(cy) => { cyRef.current = cy; }} />
                </Card>
              </>
            )}

            {activeTab === 'Community Analysis' && communityData && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={3}>
                  <Grid container spacing={2} direction="column">
                    <Grid item>
                      <Card sx={{ p: 3, textAlign: 'center' }}>
                        <Typography color="text.secondary">Total Communities</Typography>
                        <Typography variant="h3" fontWeight="bold" color="#1976d2">{communityData.total_communities}</Typography>
                      </Card>
                    </Grid>
                    <Grid item>
                      <Card sx={{ p: 3, textAlign: 'center' }}>
                        <Typography color="text.secondary">Modularity</Typography>
                        <Typography variant="h3" fontWeight="bold" color="#2e7d32">{communityData.modularity}</Typography>
                      </Card>
                    </Grid>
                    <Grid item>
                      <Card sx={{ p: 3, textAlign: 'center' }}>
                        <Typography color="text.secondary">Largest Community</Typography>
                        <Typography variant="h3" fontWeight="bold" color="#e65100">#{communityData.largest_community.community}</Typography>
                        <Typography variant="body2" color="text.secondary">{communityData.largest_community.size} members</Typography>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item xs={12} md={9}>
                  <Card sx={{ p: 2, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>Community Distribution (Top 10)</Typography>
                    <Box sx={{ height: 250, width: '100%' }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={communityData.distribution} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                          <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                          <XAxis type="number" />
                          <YAxis dataKey="community" type="category" tickFormatter={(val) => `Comm ${val}`} width={80} />
                          <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} />
                          <Bar dataKey="size" fill="#1976d2" radius={[0, 4, 4, 0]}>
                            {communityData.distribution.map((entry: any, index: number) => <Cell key={`cell-${index}`} fill={colors[entry.community % colors.length]} />)}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </Box>
                  </Card>
                </Grid>
              </Grid>
            )}

            {activeTab === 'Emotion & Sarcasm' && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Card sx={{ p: 2, height: '100%' }}>
                    <Typography variant="h6" gutterBottom>Distribusi 9 Emosi Plutchik</Typography>
                    <Box sx={{ height: 350, width: '100%', mt: 2 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        {Array.isArray(emotionData) && emotionData.length > 0 ? (
                          <BarChart data={emotionData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="emotion" angle={-45} textAnchor="end" height={70} tick={{ fill: '#666' }} />
                            <YAxis />
                            <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} contentStyle={{ borderRadius: '8px' }} />
                            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                              {emotionData.map((entry: any, index: number) => <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />)}
                            </Bar>
                          </BarChart>
                        ) : (
                          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}><Typography color="error">Data emotion tidak tersedia.</Typography></Box>
                        )}
                      </ResponsiveContainer>
                    </Box>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Grid container spacing={2} direction="column">
                    <Grid item>
                      <Card sx={{ p: 2, textAlign: 'center', backgroundColor: '#fff3e0' }}>
                        <Typography color="text.secondary" gutterBottom>Proporsi Sarcasm</Typography>
                        <Typography variant="h3" fontWeight="bold" color="#e65100">{sarcasmData?.sarcasm_percentage}%</Typography>
                        <Typography variant="body2" color="text.secondary">Dari {sarcasmData?.total_tweets} sampel tervalidasi</Typography>
                      </Card>
                    </Grid>
                    <Grid item>
                      <Card sx={{ p: 2, textAlign: 'center', backgroundColor: '#e3f2fd' }}>
                        <Typography color="text.secondary" gutterBottom>Kemunculan Emoji Sarcasm</Typography>
                        <Typography variant="h3" fontWeight="bold" color="#1565c0">{sarcasmData?.emoji_hits}</Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ fontSize: '1.5rem', mt: 1 }}>🤡 🙃 🤮 🤢 😒 💀</Typography>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            )}

            {activeTab === 'Hashtag Network' && hashtagSummary && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Card sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" gutterBottom>Hashtag Co-occurrence</Typography>
                    <Grid container spacing={2} sx={{ mb: 3 }}>
                      <Grid item xs={6}><Typography variant="h4" color="#1976d2" fontWeight="bold">{hashtagSummary.nodes}</Typography><Typography color="text.secondary">Unique Tags</Typography></Grid>
                      <Grid item xs={6}><Typography variant="h4" color="#2e7d32" fontWeight="bold">{hashtagSummary.edges}</Typography><Typography color="text.secondary">Connections</Typography></Grid>
                    </Grid>
                    <Typography variant="subtitle1" gutterBottom>Top Hashtags</Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {hashtagSummary.top_hashtags.map((h: any, i: number) => (
                        <Chip key={i} label={`${h.tag} (${h.count})`} color="primary" variant={i < 3 ? "filled" : "outlined"} onClick={() => handleNodeClick('hashtag', h.tag)} />
                      ))}
                    </Box>
                  </Card>
                </Grid>
                <Grid item xs={12} md={8}>
                  <Card sx={{ p: 2, height: '600px', position: 'relative' }}>
                    <CytoscapeComponent 
                      elements={hashtagElements} 
                      style={{ width: '100%', height: '100%' }} 
                      stylesheet={hashStylesheet} 
                      layout={{ name: 'cose', padding: 50 }} 
                      cy={(cy) => { 
                        cy.on('tap', 'node', (evt) => {
                          const node = evt.target;
                          handleNodeClick('hashtag', node.data('id'));
                        });
                      }} 
                    />
                  </Card>
                </Grid>
              </Grid>
            )}

            {activeTab === 'Emoji Network' && emojiSummary && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Card sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" gutterBottom>Emoji Co-occurrence</Typography>
                    <Grid container spacing={2} sx={{ mb: 3 }}>
                      <Grid item xs={6}><Typography variant="h4" color="#e65100" fontWeight="bold">{emojiSummary.nodes}</Typography><Typography color="text.secondary">Unique Emojis</Typography></Grid>
                      <Grid item xs={6}><Typography variant="h4" color="#1565c0" fontWeight="bold">{emojiSummary.edges}</Typography><Typography color="text.secondary">Connections</Typography></Grid>
                    </Grid>
                    <Typography variant="subtitle1" gutterBottom>Top Emojis</Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, maxHeight: '300px', overflowY: 'auto' }}>
                      {emojiSummary.top_emojis.map((e: any, i: number) => (
                        <Chip key={i} label={`${e.emoji} (${e.count})`} color="warning" variant={i < 3 ? "filled" : "outlined"} sx={{ fontSize: '1.2rem', p: 1 }} onClick={() => handleNodeClick('emoji', e.emoji)} />
                      ))}
                    </Box>
                  </Card>
                </Grid>
                <Grid item xs={12} md={8}>
                  <Card sx={{ p: 2, height: '600px', position: 'relative' }}>
                    <CytoscapeComponent 
                      elements={emojiElements} 
                      style={{ width: '100%', height: '100%' }} 
                      stylesheet={emojiStylesheet} 
                      layout={{ name: 'cose', padding: 50 }} 
                      cy={(cy) => { 
                        cy.on('tap', 'node', (evt) => {
                          const node = evt.target;
                          handleNodeClick('emoji', node.data('id'));
                        });
                      }} 
                    />
                  </Card>
                </Grid>
              </Grid>
            )}
            
            {activeTab === 'ABSA' && absaData && (
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Card sx={{ p: 3, mb: 3 }}>
                    <Typography variant="h5" gutterBottom fontWeight="bold">Aspect-Based Sentiment Analysis (ABSA)</Typography>
                    <Typography color="text.secondary" gutterBottom>
                      Menganalisis sentimen publik (Positif, Negatif, Netral) berdasarkan spesifik aspek pada program Makan Bergizi Gratis (MBG).
                    </Typography>
                  </Card>
                </Grid>

                <Grid item xs={12}>
                  <Card sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>Distribusi Sentimen per Aspek</Typography>
                    <Box sx={{ height: 400, width: '100%', mt: 2 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={absaData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                          <CartesianGrid strokeDasharray="3 3" vertical={false} />
                          <XAxis dataKey="aspect" />
                          <YAxis />
                          <Tooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} contentStyle={{ borderRadius: '8px' }} />
                          <Legend />
                          <Bar dataKey="positif" name="Positif" stackId="a" fill="#4caf50" radius={[0, 0, 0, 0]} />
                          <Bar dataKey="netral" name="Netral" stackId="a" fill="#9e9e9e" radius={[0, 0, 0, 0]} />
                          <Bar dataKey="negatif" name="Negatif" stackId="a" fill="#f44336" radius={[4, 4, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </Box>
                  </Card>
                </Grid>
                
              </Grid>
            )}

          </>
        )}
      </Box>
    </Box>
  );
}
